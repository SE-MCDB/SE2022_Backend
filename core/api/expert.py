from core.models.expert import Expert
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest
from .utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.api.auth import jwt_auth
from core.models.user import User


@response_wrapper
@require_http_methods('POST')
def setinfo(request:HttpRequest):
    id = request.POST.get("id", None)
    if not id:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need valid id")
    name = request.POST.get("name", None)
    if not name:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need valid name")
    paper = request.POST.get("paper", None)
    patent = request.POST.get("patent", None)
    if not patent and not paper:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need at least one paper or patent")
    organization = request.POST.get("organization", None)
    if not organization:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need valid organization")
    field = request.POST.get("field", None)
    if not field:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need valid field")
    ID_num = request.POST.get("ID_num", None)
    if not ID_num:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need valid ID_num")
    scholar_ID = request.FILES.get("scholar_ID", None)
    scholar_profile = request.POST.get("scholar_profile", None)
    if not scholar_profile:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need valid scholar_profile")
    phone = request.POST.get("phone", None)
    if not phone:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need valid phone")
    user = User.objects.get(id=id)
    if user.state == 4:
        expert = user.expert_info
        expert.name = name
        expert.organization = organization
        expert.field = field
        expert.ID_num = ID_num
        expert.ID_pic = scholar_ID
        expert.self_profile = scholar_profile
        expert.phone = phone
        expert.save()
        user.save()
    else:
        expert = Expert()
        expert.name = name
        expert.organization = organization
        expert.field = field
        expert.ID_num = ID_num
        expert.ID_pic = scholar_ID
        expert.self_profile = scholar_profile
        expert.phone = phone
        expert.save()
        user.expert_info = expert
        user.state = 4
        user.save()
    return success_api_response("correct")


"""
应该添加一个认证成功提示
"""
#@jwt_auth()
@response_wrapper
@require_http_methods('GET')
def agree_expert(request:HttpRequest, id:int):
    data = request.GET.dict()
    scholarID = data.get('scholarID')
    url = data.get('url')
    print(scholarID)
    print(url)
    print(id)
    user = User.objects.get(id=id)
    if user.state != 1:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "invalid user state")
    user.state = 4
    expert_info = user.expert_info
    expert_info.scholarID = scholarID
    expert_info.url = url
    expert_info.save()
    user.save()
    return success_api_response({})


"""
应该添加一个认证失败提示
对于专家信息的删除可能有bug，这里需要测试一下
"""
@jwt_auth()
@response_wrapper
@require_http_methods('GET')
def refuse_expert(request:HttpRequest, id:int):
    user = User.objects.get(id=id)
    if user.state != 1:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "invalid user state")
    user.expert_info.delete()
    user.state = 0
    user.save()
    return success_api_response({})


"""
通过id获得相应用户申请成为企业的信息
"""
@jwt_auth()
@response_wrapper
@require_http_methods('GET')
def get_expertInfo(request:HttpRequest, id:int):
    user = User.objects.get(id=id)
    if user.state != 1:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "invalid user state")
    expert_info = user.expert_info
    return success_api_response({
        "name": expert_info.name,
        "ID_num": expert_info.ID_num,
        "organization": expert_info.organization,
        "field": expert_info.field,
        "self_profile": expert_info.self_profile,
        "phone": expert_info.phone,
        "ID_pic": str(expert_info.ID_pic)
    })
