from curses.ascii import HT
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import HttpRequest
from numpy import require
from pytz import timezone
import functools

from sqlalchemy import desc
from core.api.utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.models.user import User
from core.models.enterprise_info import Enterprise_info
from core.api.auth import jwt_auth
from core.models.need import Need
from core.models.order import Order
from django.utils import timezone
from core.models.rate import Rate


@response_wrapper
# @jwt_auth()
@require_POST
def rate_order(request: HttpRequest):
    data = parse_data(request=request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "cannot find data")

    formData = data.get('formData')

    if not formData:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "cannot find formData")

    rate_taste = formData.get('rate_taste')
    rate_speed = formData.get('rate_speed')
    rate_level = formData.get('rate_level')
    description = formData.get('description')
    datetime = formData.get('datetime')
    order_id = formData.get('order_id')

    if not rate_taste or not rate_speed or not rate_level or not datetime or not order_id:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "parameter wrong")

    try:
        order = Order.objects.get(id=order_id)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "cannot find orderid")

    rate = Rate(rate_taste=rate_taste, rate_speed=rate_speed, rate_level=rate_level, 
        datetime=datetime, order_id=order_id, expert_id=order.user_id, enterprise_id=order.enterprise_id)

    if description:
        rate.description = description
    rate.save()
    return success_api_response({})