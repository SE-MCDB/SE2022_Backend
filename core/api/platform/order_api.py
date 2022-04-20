from cmath import exp
from re import S
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import HttpRequest

from core.api.utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.models.user import User
from core.models.enterprise_info import Enterprise_info
from core.api.auth import jwt_auth
from core.models.need import Need
from core.models.order import Order

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
    try:
        user: User = User.objects.get(id=uid)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")
    
    
    if user.state == 5:
        # 企业
        order_list = user.enterprise_order.filter(state__in=[2, 3])
    elif user.state == 4:
        # 专家
        order_list = user.expert_order.filter(state__in=[2, 3])
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "user type is not expert or company")
    
    orders = []
    for order in order_list:
        expert: User = order.user
        enterprise: User = order.enterprise
        need: Need = order.need
        order_info = {"order_id": order.id, "create_time": order.create_time, "end_time": order.end_time,
            "state": order.state, "expert_id":expert.id, "expert_name": expert.username, "need":{
                "need_id": need.id,
                "title": need.title,
                "enterprise_id": enterprise.id,
                "enterprise_name": enterprise.enterprise_info.name
            }}
        orders.append(order_info)

    return success_api_response({"data":orders})



@response_wrapper
# @jwt_auth()
@require_GET
def get_pending_order(request: HttpRequest, uid: int):
    """
    get proceding order

    [method]: GET

    parms:
        - uid: 企业或专家的id
    """
    try:
        user: User = User.objects.get(id=uid)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")
    
    
    if user.state == 5:
        # 企业
        order_list = user.enterprise_order.filter(state=0)
    elif user.state == 4:
        # 专家
        order_list = user.expert_order.filter(state=0)
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "user type is not expert or company")
    
    orders = []
    for order in order_list:
        expert: User = order.user
        enterprise: User = order.enterprise
        need: Need = order.need
        order_info = {"order_id": order.id, "create_time": order.create_time, "end_time": order.end_time,
            "state": order.state, "expert_id":expert.id, "expert_name": expert.username, "need":{
                "need_id": need.id,
                "title": need.title,
                "enterprise_id": enterprise.id,
                "enterprise_name": enterprise.enterprise_info.name
            }}
        orders.append(order_info)

    return success_api_response({"data": orders})

@response_wrapper
# @jwt_auth()
@require_GET
def get_cooperating_order(request: HttpRequest, uid: int):
    """
    get proceding order

    [method]: GET

    parms:
        - uid: 企业或专家的id
    """
    try:
        user: User = User.objects.get(id=uid)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")
    
    
    if user.state == 5:
        # 企业
        order_list = user.enterprise_order.filter(state=1)
    elif user.state == 4:
        # 专家
        order_list = user.expert_order.filter(state=1)
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "user type is not expert or company")
    
    orders = []
    for order in order_list:
        expert: User = order.user
        enterprise: User = order.enterprise
        need: Need = order.need
        order_info = {"order_id": order.id, "create_time": order.create_time, "end_time": order.end_time,
            "state": order.state, "expert_id":expert.id, "expert_name": expert.username, "need":{
                "need_id": need.id,
                "title": need.title,
                "enterprise_id": enterprise.id,
                "enterprise_name": enterprise.enterprise_info.name
            }}
        orders.append(order_info)

    return success_api_response({"data": orders})


""" path('order', create_order),  # 企业创建新订单
    path('order/<int:id>', get_order_info), # 获取某个订单的信息
    path('user/<int:uid>/order/<int:id>/refuse', refuse_order), # 专家拒绝订单
    path('user/<int:uid>/order/<int:id>/accept', accept_order), # 专家接受订单
    path('user/<int:uid>/order/<int:id>/finish', finish_order), # 企业结束订单
ok  path('user/<int:uid>/order/finished', get_finished_order), # 获取某个用户（企业或专家）已完成订单（拒绝和结束）
ok  path('user/<int:uid>/order/pending', get_pending_order), # 获取某个用户（企业或专家）新请求的订单
ok  path('user/<int:uid>/order/cooperating', get_cooperating_order), # 获取某个用户（企业或专家）正在合作的订单
"""

@response_wrapper
# @jwt_auth()
@require_POST
def finish_order(request: HttpRequest, uid: int, id: int):
    try:
        enterprise: User = User.objects.get(id=uid)
        order: Order = Order.objects.get(id=id)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist enterprise")
    except Order.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist order")
    
    if order.enterprise != enterprise:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "not the enterprise's order")

    if enterprise.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")

    if order.state == 1 or order.state == 0:
        Order.objects.filter(id=id).update(state=3)
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "The order is not in cooperation")

    return success_api_response({})


@response_wrapper
# @jwt_auth()
@require_POST
def accept_order(request: HttpRequest, uid: int, id: int):
    """
    expert accept the order
    turn state=0 to state=1
    """
    try:
        expert: User = User.objects.get(id=uid)
        order: Order = Order.objects.get(id=id)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist expert")
    except Order.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist order")
    
    if order.user != expert:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "not the expert's order")

    if expert.state != 4:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-expert user")

    if order.state == 0:
        Order.objects.filter(id=id).update(state=1)
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "The order is not pending state(state=0)")

    need: Need = order.need 
    need.real = need.real + 1
    need.save()
    return success_api_response({})


@response_wrapper
# @jwt_auth()
@require_POST
def refuse_order(request: HttpRequest, uid: int, id: int):
    """
    expert accept the order
    turn state=0 to state=1
    """
    try:
        expert: User = User.objects.get(id=uid)
        order: Order = Order.objects.get(id=id)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist expert")
    except Order.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist order")
    
    if order.user != expert:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "not the expert's order")

    if expert.state != 4:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-expert user")

    if order.state == 0:
        Order.objects.filter(id=id).update(state=2)
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "The order is not pending state(state=0)")
    return success_api_response({})


@response_wrapper
# @jwt_auth()
@require_GET
def get_order_info(request: HttpRequest, id: int):
    try:
        order: Order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist order")
    
    expert: User = order.user
    enterprise: User = order.enterprise
    need: Need = order.need
    order_info = {"order_id": order.id, "create_time": order.create_time, "end_time": order.end_time,
        "address": need.address, "description": need.description, "phone": enterprise.enterprise_info.phone,
        "predict": need.predict, "real": need.real,
        "state": order.state, "expert_id":expert.id, "expert_name": expert.username, "need":{
            "need_id": need.id,
            "title": need.title,
            "enterprise_id": enterprise.id,
            "enterprise_name": enterprise.enterprise_info.name
        }}

    return success_api_response(order_info)


@response_wrapper
# @jwt_auth()
@require_POST
def create_order(request: HttpRequest):
    data = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")


    need_id = data.get("need_id")
    expert_id = data.get("expert_id")
    enterprise_id = data.get("enterprise_id")
    print(need_id, expert_id, enterprise_id)
    try:
        need = Need.objects.get(id=need_id)
        expert = User.objects.get(id=expert_id)
        enterprise = User.objects.get(id=enterprise_id)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "cannot find need or expert or enterprise obj")
    
    if expert.state != 4:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-expert user")
    if enterprise.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")
    if need.state != 0:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "the need is finished")

    order: Order = Order(user_id=expert_id, enterprise_id=enterprise_id, need_id=need_id, state=0)
    order.save()
    return success_api_response({})