import torch
from django.http import HttpRequest
from django.views.decorators.http import require_GET

from core.api.utils import (response_wrapper, success_api_response)
from core.models.papers import Papers
from core.models.need import Need
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
from core.api.auth import getUserInfo
from core.api.milvus_utils import get_milvus_connection, milvus_search, milvus_query_by_id
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
    id_lists = milvus_search(collection_name="O2E_TEMP", query_vectors=b, topk=3,
                             partition_names=None)[0]
    register_experts = []
    scholarIDs = []
    for id in id_lists:
        paper = Papers.objects.get(vector=str(id))
        expert_possible = paper.expert_papers.all()
        for expert in expert_possible:
            scholarIDs.append(expert.scholarID)
            user = expert.expert_info
            register_experts.append(getUserInfo(user))

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
    paper_ids = milvus_query_by_id(query)
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
        "register": register_experts,
        "other": possible_experts
    })