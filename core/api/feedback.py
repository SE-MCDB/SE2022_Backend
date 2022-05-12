from django.views.decorators.http import require_http_methods
from django.http import HttpRequest
from .utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.models.feedback import Feedback


@response_wrapper
#@jwt_auth()
@require_http_methods('GET')
def get_feedback(request:HttpRequest):
    feedbacks = Feedback.objects.all()
    datas = []
    for feedback in feedbacks:
        data = {
            "name": feedback.name,
            "email": feedback.email,
            "sex": get_sex(feedback.sex),
            "qtype": get_type(feedback.qtype),
            "description": feedback.description,
            "datatime": feedback.dataTime
        }
        datas.append(data)
    return success_api_response({"data": datas})


def get_sex(sex):
    if sex == 0:
        return "男"
    elif sex == 1:
        return "女"
    else:
        return "未知"


def get_type(qtype):

    dic = {
        0: "订单相关",
        1: "支付相关",
        2: "账号相关",
        3: "安全相关",
        4: "反馈建议",
        5: "其他"
    }

    types = list(qtype)
    print(types)
    ans = []
    i = 0
    while i < 6:
        if types[i] == '1':
            ans.append(dic[i])
        i += 1
    return ans


@response_wrapper
#@jwt_auth()
@require_http_methods('POST')
def make_feedback(request:HttpRequest):
    name = request.GET.get("name")
    email = request.GET.get("email")
    sex = request.GET.get("sex")
    qtype_temp = request.GET.get("qtype")
    qtype = get_qtype(qtype_temp)
    description = request.GET.get("description")
    feedback = Feedback()
    feedback.name = name
    feedback.email = email
    feedback.sex = sex
    feedback.qtype = qtype
    feedback.description = description
    feedback.save()
    return success_api_response("success")


def get_qtype(qtype_temp):
    l = ['0', '0', '0', '0', '0', '0']
    for qtype in qtype_temp:
        l[qtype] = '1'
    return ''.join(l)
