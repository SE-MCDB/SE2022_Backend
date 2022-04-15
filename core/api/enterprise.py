from core.models.enterprise_info import Enterprise_info
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest
from .utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.api.auth import jwt_auth
from core.models.image import Image
from core.models.user import User


@jwt_auth()
@response_wrapper
@require_http_methods('POST')
def set_info(request:HttpRequest):
    data: dict = parse_data(request)

    id = data['id']
    if not id:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "lack user id")

    name = data['name']
    if not name:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "lack enterprise name")

    address = data['address']
    if not address:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "lack address")

    website = data['website']
    if not website:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "lack website")

    instruction = data['instruction']
    if not instruction:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "lack instruction")

    phone = data['phone']
    if not phone:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "lack enterprise phoneNum")

    legal_representative = data['legal_representative']
    if not legal_representative:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "lack legal_representative")

    register_capital = data['register_capital']
    if not register_capital:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "lack register_capital")

    field = data['field']
    if not field:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "lack field")
    dic = {
        'id': id,
        'name': name,
        'address': address,
        'website': website,
        'instruction': instruction,
        'phone': phone,
        'legal_representative': legal_representative,
        'register_capital': register_capital,
        'field': field
    }
    return success_api_response(dic)