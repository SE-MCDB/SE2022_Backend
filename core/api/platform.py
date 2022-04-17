from ast import keyword
import re
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import HttpRequest

from .utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.models.user import User
from core.api.auth import jwt_auth
from core.models.need import Need


@response_wrapper
# @jwt_auth()
@require_POST
def create_need(request: HttpRequest):
    """
    create need

    [method]: POST

    [route]: /api/need
    
    parms:
		- 
    """
    data = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    user: User = request.user
    title = data.get('title')
    description = data.get('description')
    money = data.get('money')
    valid_time = data.get('valid_time')
    key_word = data.get('key_word') 
    field = data.get('field')
    address = data.get('address')
    state = data.get('state')
    emergency = data.get('emergency')
    predict = data.get('predict')
    
    need = Need(title=title, description=description, money=money,
    valid_time=valid_time, key_word=key_word, field=field, address=address,
    enterprise=user, state=state, emergency=emergency, predict=predict)
    need.save()
    return success_api_response({})

@response_wrapper
# @jwt_auth()
@require_GET
def get_all_need(request: HttpRequest):
    """
    get all need whose state == 0

    """
    needs = Need.objects.filter(state=0)
    
    data = []
    for need in needs:
        need_info = {"need_id" : need.id, "title": need.title, "description": need.description,
        "valid_time": need.valid_time, "field": need.field, "state": need.state, "emergency": need.emergency}
        data.append(need_info)
    return success_api_response(data)

def get_finished_order(request: HttpRequest, uid: int):
    """
    get finished order

    [method]: GET

    parms:
        - uid: 企业或专家的id 
    """
    


# @response_wrapper
# @jwt_auth()
# @require_http_methods('POST')
# def createCollect(request: HttpRequest):
#     data : dict = parse_data(request)
#     id = data.get("id") # 论文解读id
#     uid = data.get("uid") # 用户id
#     ret = {
#         'id': 233,  # main key id of interpretation
#     }
#     return success_api_response(ret)
