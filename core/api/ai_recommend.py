import torch
from django.http import HttpRequest
from django.views.decorators.http import require_GET

from core.api.utils import (response_wrapper, success_api_response)
from core.models.papers import Papers
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel

import numpy

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


@response_wrapper
@require_GET
def experiment(request:HttpRequest):
    papers = Papers.objects.all()
    for paper in papers:
        embed = model.get_embeds(paper.title)
        embed = embed / embed.norm(dim=1, keepdim=True)
        array = embed.detach().numpy()[0]
        s = ','.join([str(f) for f in array])
        paper.vector = s
        paper.save()
    return success_api_response("success")


@response_wrapper
@require_GET
def recommend(request:HttpRequest):
    keyword = ["net;deep learning"]
    key_vector = model.get_embeds(keyword)
    key_vector = key_vector / key_vector.norm(dim=1, keepdim=True)
    b = key_vector.detach().numpy()
    papers = Papers.objects.all()
    a = numpy.zeros(shape=(len(papers), 128))
    index = 0
    list1 = []
    list2 = []
    for paper in papers:
        list1.append(paper.id)
        vector = paper.vector
        list = vector.split(',')
        i = 0
        while i < 128:
            list[i] = float(list[i])
            i += 1
        a[index] = list
        index += 1

    result = numpy.matmul(a, b.T)

    #假设取前三高的人作为被推荐专家
    i = 0
    while i < len(papers):
        list2.append(result[i][0])
        i += 1

    temp1 = 0
    while temp1 < len(papers):
        temp2 = temp1 + 1
        while temp2 < len(papers):
            if list2[temp1] < list2[temp2]:
                temp = list2[temp1]
                list2[temp1] = list2[temp2]
                list2[temp2] = temp
                temp = list1[temp1]
                list1[temp1] = list1[temp2]
                list1[temp2] = temp
            temp2 += 1
        temp1 += 1
    print(list2)
    print(list1)
    return success_api_response("success")







