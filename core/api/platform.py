from ast import keyword
from curses import ERR
import re
from urllib import response
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import HttpRequest

from .utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.models.user import User
from core.models.enterprise_info import Enterprise_info
from core.api.auth import jwt_auth
from core.models.need import Need

@response_wrapper
# @jwt_auth()
@require_GET
def get_need_info(request: HttpRequest, id: int):
    need = Need.objects.filter(id=id)[0]
    if not need:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "cannot find need id")
    
    enterprise : User = need.enterprise
    enterprise_info : Enterprise_info = enterprise.enterprise_info

    need_info = {"title": need.title, "description": need.description, "money": need.money, "start_time": need.start_time, 
    "valid_time": need.valid_time, "key_word": need.key_word, "field": need.field, "address": need.address, "state": need.state, 
    "emergency": need.emergency, "predict": need.predict, "real": need.real, "enterprise_id": enterprise.id, "enterprise_name": enterprise_info.name}

    return success_api_response(need_info)

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
    data:dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    user: User = User.objects.filter(id=data.get('company_id'))[0]

    if user.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "User is not Company")


    title = data.get('title')
    description = data.get('description')
    money = data.get('money')
    start_time = data.get('start_time')
    valid_time = data.get('valid_time')
    key_word = data.get('key_word') 
    field = data.get('field')
    address = data.get('address')
    state = data.get('state')
    emergency = data.get('emergency')
    predict = data.get('predict')
    
    need = Need(title=title, description=description, money=money, start_time=start_time,
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
    return success_api_response({"data": data})



@response_wrapper
# @jwt_auth()
@require_GET
def get_finished_order(request: HttpRequest, uid: int):
    """
    get finished order

    [method]: GET

    parms:
        - uid: 企业或专家的id 
    """ 
    user: User = User.objects.filter(id=uid)
    if user is None:   
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid user id")
    orders = []
    if user.user_type == 2:
        # 企业
        # need_list = 
        pass
    elif user.user_type == 1:
        # 专家
        order_list = user.order_set.filter(state=1)
        for order in order_list:
            order_info = {}
            orders.append(order_info)


    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "user type is not college or company")

    return success_api_response(orders)



@response_wrapper
# @jwt_auth()
@require_GET
def get_proceding_order(request: HttpRequest, uid: int):
    """
    get proceding order

    [method]: GET

    parms:
        - uid: 企业或专家的id
    """
    user: User = User.objects.filter(id=uid)
    



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
