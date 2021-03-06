import torch
from django.db.models import Avg
from django.http import HttpRequest
from django.views.decorators.http import require_GET

from core.api.utils import (response_wrapper, success_api_response)
from core.models.papers import Papers
from core.models.need import Need
from core.models.user import User
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
from core.api.auth import getUserInfo
from core.api.milvus_utils import get_milvus_connection, milvus_search, milvus_query_paper_by_id, milvus_query_need_by_id, milvus_insert
from core.api.zhitu_utils import get_expertInfo_by_expertId, search_expertID_by_paperID


class ContrastiveSciBERT(nn.Module):
    def __init__(self, out_dim, tau, device='cpu'):
        """⽤于对⽐学习的SciBERT模型
        :param out_dim: int 输出特征维数
        :param tau: float 温度参数τ
        :param device: torch.device, optional 默认为CPU
        """
        super().__init__()
        self.tau = tau
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')
        self.model = AutoModel.from_pretrained('allenai/scibert_scivocab_uncased').to(device)
        self.linear = nn.Linear(self.model.config.hidden_size, out_dim).to(device)

    def get_embeds(self, texts, max_length=64):
        """将⽂本编码为向量
        :param texts: List[str] 输⼊⽂本列表，⻓度为N


        # Press the green button in the gutter to run the script.
        if __name__ == '__main__':
            print("success")
        :param max_length: int, optional padding最⼤⻓度，默认为64
        :return: tensor(N, d_out)
        """
        encoded = self.tokenizer(
            texts, padding='max_length', truncation=True, max_length=max_length, return_tensors='pt'
        ).to(self.device)
        return self.linear(self.model(**encoded).pooler_output)

    def calc_sim(self, texts_a, texts_b):
        """计算两组⽂本的相似度
        :param texts_a: List[str] 输⼊⽂本A列表，⻓度为N
        :param texts_b: List[str] 输⼊⽂本B列表，⻓度为N
        :return: tensor(N, N) 相似度矩阵，S[i, j] = cos(a[i], b[j]) / τ
        """
        embeds_a = self.get_embeds(texts_a)  # (N, d_out)
        embeds_b = self.get_embeds(texts_b)  # (N, d_out)
        embeds_a = embeds_a / embeds_a.norm(dim=1, keepdim=True)
        embeds_b = embeds_b / embeds_b.norm(dim=1, keepdim=True)
        return embeds_a @ embeds_b.t() / self.tau

    def forward(self, texts_a, texts_b):
        """计算两组⽂本的对⽐损失（直接返回损失）
        :param texts_a: List[str] 输⼊⽂本A列表，⻓度为N
        :param texts_b: List[str] 输⼊⽂本B列表，⻓度为N
        :return: tensor(N, N), float A对B的相似度矩阵，对⽐损失
        """
        # logits_ab等价于预测概率，对⽐损失等价于交叉熵损失
        logits_ab = self.calc_sim(texts_a, texts_b)
        logits_ba = logits_ab.t()
        labels = torch.arange(len(texts_a), device=self.device)
        loss_ab = F.cross_entropy(logits_ab, labels)
        loss_ba = F.cross_entropy(logits_ba, labels)
        loss = (loss_ab + loss_ba) / 2
        return loss


model = torch.load("model.pt")


@require_GET
@response_wrapper
def recommend(request: HttpRequest, id: int):
    get_milvus_connection()
    need = Need.objects.get(id=id)
    keyword = [need.key_word]
    key_vector = model.get_embeds(keyword)
    key_vector = key_vector / key_vector.norm(dim=1, keepdim=True)
    b = key_vector.detach().numpy().tolist()
    id_lists = milvus_search(collection_name="O2E_TEMP", query_vectors=b, topk=10,
                             partition_names=None)[0]
    cites = []
    register_experts = []
    scholarIDs = []
    for id in id_lists:
        paper = Papers.objects.get(vector=str(id))
        title = paper.title
        expert_possible = paper.expert_papers.all()
        for expert in expert_possible:
            cite = 0
            papers = expert.papers.all()
            for paper in papers:
                cite += paper.cites
            cites.append(cite)
            scholarIDs.append(expert.scholarID)
            user = expert.expert_info
            dic = getUserInfo(user)
            dic['title'] = title
            avg = list()
            avg_taste = user.expert_rate.aggregate(Avg('rate_taste')).get('rate_taste__avg')
            if avg_taste is None:
                avg_taste = 5
            avg.append(avg_taste)

            avg_speed = user.expert_rate.aggregate(Avg('rate_speed')).get('rate_speed__avg')
            if avg_speed is None:
                avg_speed = 5
            avg.append(avg_speed)

            avg_level = user.expert_rate.aggregate(Avg('rate_level')).get('rate_level__avg')
            if avg_level is None:
                avg_level = 5
            avg.append(avg_level)
            dic['comment'] = avg
            register_experts.append(dic)
    max_cite = max(cites)
    i = 0
    while i < len(register_experts):
        j = i + 1
        while j < len(register_experts):
            if max_cite != 0:
                score_i = sum(register_experts[i]["comment"]) + cites[i] / max_cite
                score_j = sum(register_experts[j]["comment"]) + cites[j] / max_cite
            else:
                score_i = sum(register_experts[i]["comment"]) + cites[i]
                score_j = sum(register_experts[j]["comment"]) + cites[j]
            if score_j > score_i:
                temp = register_experts[i]
                register_experts[i] = register_experts[j]
                register_experts[j] = temp
            j += 1
        i += 1

    #未注册专家推荐
    possible_experts = []
    id_lists = milvus_search(collection_name="O2E_ALL", query_vectors=b, topk=3, partition_names=None)[0]
    s = '['
    for id in id_lists:
        s = s + str(id) + ','
    if len(s) != 1:
        s = s[:-1]
    s += ']'
    query = "milvus_id in " + s
    paper_ids = milvus_query_paper_by_id(query)
    for paper_id in paper_ids:
        num = 0
        expert_ids, title = search_expertID_by_paperID(paper_id['paper_id'])
        for expert_id in expert_ids:
            op = True
            for scholarID in scholarIDs:
                if expert_id == scholarID:
                    op = False
                    break
            if op and num < 3:
                num += 1
                expert_list = get_expertInfo_by_expertId(expert_id)
                expert_list['title'] = title
                possible_experts.append(expert_list)
    return success_api_response({
        "register": register_experts[:3],
        "other": possible_experts[:3]
    })


@require_GET
@response_wrapper
def need_recommend(request:HttpRequest, id:int):
    get_milvus_connection()
    user = User.objects.get(id=id)
    papers = user.expert_info.papers.all()
    titles = []
    for paper in papers:
        titles.append(paper.title)
    key_vector = model.get_embeds(titles)
    key_vector = key_vector / key_vector.norm(dim=1, keepdim=True)
    key_vector = key_vector.detach().numpy().tolist()
    id_lists = milvus_search("O2E_NEED", query_vectors=key_vector, topk=2, partition_names=None)
    ids = '['
    for id_list in id_lists:
        for milvus_id in id_list:
            ids += str(milvus_id) + ','
    ids = ids[:-1] + ']'
    query = "milvus_id in "+ ids
    need_ids = milvus_query_need_by_id(query)
    need_infos = []
    for need_id in need_ids:
        need = Need.objects.get(pk=need_id['need_id'])
        if need.state == 0:
            enterprise: User = need.enterprise
            need_info = {
                "need_id": need.id, "title": need.title, "description": need.description, "money": need.money,
                "start_time": need.start_time,
                "end_time": need.end_time, "key_word": need.key_word, "field": need.field, "address": need.address,
                "state": need.state,
                "emergency": need.emergency,
                "enterprise_id": enterprise.id, "enterprise_name": enterprise.enterprise_info.name,
                "enterprise_pic": str(enterprise.icon)
            }
            order = list()
            orders = need.need_order.exclude(state=2)
            for o in orders:
                order_info = {
                    "order_id": o.id,
                    "order_state": o.state,
                    "expert_id": o.user.id,
                    "expert_icon": str(o.user.icon),
                    "expert_name": o.user.expert_info.name,
                    "enterprise_id": o.enterprise.id
                }
                order.append(order_info)
            need_info['order'] = order
            need_infos.append(need_info)

    return success_api_response({"needs": need_infos[:3]})


def insert_need(nid: int):
    get_milvus_connection()
    need = Need.objects.get(pk=nid)
    keyword = [need.key_word]
    key_vector = model.get_embeds(keyword)
    key_vector = key_vector / key_vector.norm(dim=1, keepdim=True)
    key_vector = key_vector.detach().numpy().tolist()
    milvus_id = milvus_insert("O2E_NEED", [key_vector, [nid]])
    print(milvus_id)
    return True
