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


