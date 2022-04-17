from core.models.enterprise_info import Enterprise_info
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest
from .utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.api.auth import jwt_auth
from core.models.user import User


#@jwt_auth()
@response_wrapper
@require_http_methods('POST')
def set_info(request:HttpRequest):
    id = request.POST.get("id", None)
    print(id)
    if not id:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid id")
    name = request.POST.get('name', None)
    print(name)
    if not name:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid name")
    address = request.POST.get('address', None)
    print(address)
    if not address:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid address")
    website = request.POST.get("website", None)
    print(website)
    if not website:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid website")
    instruction = request.POST.get("instruction", None)
    print(instruction)
    if not instruction:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid instruction")
    phone = request.POST.get("phone", None)
    print(phone)
    if not phone:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid phone")
    legal_representative = request.POST.get("legal_representative", None)
    print(legal_representative)
    if not legal_representative:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid legal_representative")
    register_capital = request.POST.get("register_capital", None)
    print(register_capital)
    if not register_capital:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid register_capital")
    field = request.POST.get("field", None)
    print(field)
    if not field:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid field")
    business_license = request.FILES.get("business_license", None)
    if not business_license:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid business_license")
    legal_person_ID = request.FILES.get("legal_person_ID", None)
    if not legal_person_ID:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "need a valid legal_person_ID")

    user = User.objects.get(id=id)
    if user.state == 0:
        enterprise_info = Enterprise_info()
        enterprise_info.name = name
        enterprise_info.address = address
        enterprise_info.website = website
        enterprise_info.instruction = instruction
        enterprise_info.phone = phone
        enterprise_info.legal_representative = legal_representative
        enterprise_info.register_capital = register_capital
        enterprise_info.field = field
        enterprise_info.business_license = business_license
        enterprise_info.legal_person_ID = legal_person_ID
        enterprise_info.save()
        user.enterprise_info = enterprise_info
        user.state = 5
        user.save()
    elif user.state == 5:
        enterprise_info = user.enterprise_info
        enterprise_info.name = name
        enterprise_info.address = address
        enterprise_info.website = website
        enterprise_info.instruction = instruction
        enterprise_info.phone = phone
        enterprise_info.legal_representative = legal_representative
        enterprise_info.register_capital = register_capital
        enterprise_info.field = field
        enterprise_info.business_license = business_license
        enterprise_info.legal_person_ID = legal_person_ID
        enterprise_info.save()
        user.save()

    return success_api_response("enterprise register successfully")


@jwt_auth()
@response_wrapper
@require_http_methods('POST')
def get_info(request:HttpRequest):
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    id = data.get("id")
    user = User.objects.get(id=id)
    enterprise_info = user.enterprise_info
    dic = {
        "name": enterprise_info.name,
        "address": enterprise_info.address,
        "website": enterprise_info.website,
        "instruction": enterprise_info.instruction,
        "phone": enterprise_info.phone,
        "legal_representative": enterprise_info.legal_representative,
        "register_capital": enterprise_info.register_capital,
        "field": enterprise_info.field,
    }
    return success_api_response(dic)