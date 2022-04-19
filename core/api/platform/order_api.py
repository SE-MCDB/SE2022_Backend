from ast import keyword
from curses import ERR
import re
from urllib import response
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import HttpRequest

from core.api.utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.models.user import User
from core.models.enterprise_info import Enterprise_info
from core.api.auth import jwt_auth
from core.models.need import Need

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
    user: User = User.objects.filter(id=uid)[0]
    if not user:   
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid user id")
    
    orders = []
    
    if user.state == 5:
        # 企业
        order_list = user.enterprise_order.filter(state=1)
        for order in order_list:
            order_info = {}
            orders.append(order_info)
        orders.append(1)
    elif user.state == 4:
        # 专家
        order_list = user.expert_order.filter(state=1)
        for order in order_list:
            order_info = {}
            orders.append(order_info)
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "user type is not expert or company")
    return success_api_response(orders)



@response_wrapper
# @jwt_auth()
@require_GET
def get_proceeding_order(request: HttpRequest, uid: int):
    """
    get proceding order

    [method]: GET

    parms:
        - uid: 企业或专家的id
    """
    user: User = User.objects.filter(id=uid)
    



def finish_order(request: HttpRequest):
    pass


def accept_order(request: HttpRequest):
    pass 



def refuse_order(request: HttpRequest):

    pass


def get_order_info(request: HttpRequest):
    pass


def create_order(request: HttpRequest):
    pass