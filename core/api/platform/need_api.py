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
def get_need_info(request: HttpRequest, id: int):
    try:
        need = Need.objects.get(id=id)
    except Need.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist need")

    enterprise : User = need.enterprise

    need_info = {"title": need.title, "description": need.description, "money": need.money, "start_time": need.start_time, 
    "end_time": need.end_time, "key_word": need.key_word, "field": need.field, "address": need.address, "state": need.state, 
    "emergency": need.emergency, "predict": need.predict, "real": need.real, "enterprise_id": enterprise.id, "enterprise_name": enterprise.enterprise_info.name}

    return success_api_response(need_info)

@response_wrapper
# @jwt_auth()
@require_POST
def create_need(request: HttpRequest):
    """
    create need

    [method]: POST

    [route]: /api/need
    """
    data:dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "data int none")

    id = data.get('company_id')
    if not id:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "id not found")

    try:
        user: User = User.objects.get(id=id)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")

    if user.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")


    title = data.get('title')
    description = data.get('description')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    key_word = data.get('key_word') 
    address = data.get('address')

    try:
        money = int(data.get('money'))
        predict = int(data.get('predict'))
        real = int(data.get('real'))
        emergency = int(data.get('emergency'))
        state = int(data.get('state'))
        field = int(data.get('field'))
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-digit value(some digit value is wrong)")

    print("title", title)
    print("descrption", description)
    print("money", money)
    print("start_time", start_time)
    print("end_time", end_time)
    print("key_word", key_word)
    print("field", field)
    print("address", address)
    print("emergency", emergency)
    print("predict", predict)
    print("real", real)
    print("state", state)


    if title is None or description is None or money is None or start_time is None  or end_time is None or key_word is None \
        or field is None or address is None or emergency is None or predict is None or real is None  or state is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid requset value")
    
    if not title or not description or not start_time:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "title or description or start_time cannot be empty")

    need = Need(title=title, description=description, money=money, start_time=start_time,
        end_time=end_time, key_word=key_word, field=field, address=address,
            enterprise=user, state=state, emergency=emergency, predict=predict, real=real)
    
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
        "end_time": need.end_time, "field": need.field, "state": need.state, "emergency": need.emergency, "predict": need.predict,"real": need.real}
        data.append(need_info)
    return success_api_response({"data": data})


@response_wrapper
# @jwt_auth()
@require_GET
def get_finished_need(request: HttpRequest, uid: int):
    """
    get user(id = uid, enterprise) finished need
    """
    try:
        user: User = User.objects.get(id=uid)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")

    if user.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")

    needs = user.enterprise_need.filter(state=1)
    data = []
    for need in needs:
        need_info = {"need_id" : need.id, "title": need.title, "description": need.description,
        "end_time": need.end_time, "field": need.field, "state": need.state, "emergency": need.emergency, "predict": need.predict,"real": need.real}
        data.append(need_info)
    
    return success_api_response({"data": data})


@response_wrapper
# @jwt_auth()
@require_POST
def finish_need(request: HttpRequest, uid: int, id: int):
    try:
        user: User = User.objects.get(id=uid)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")

    if user.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")

    try:
        need: Need = Need.objects.get(id=id)
    except Need.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist need")

    if need.enterprise != user:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Not the enterprise's need")
    Need.objects.filter(id=id).update(state=1)
    return success_api_response({})


@response_wrapper
# @jwt_auth()
@require_GET
def get_proceeding_need(request: HttpRequest, uid: int):
    try:
        user: User = User.objects.get(id=uid)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")
    
    if user.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")
    needs = user.enterprise_need.filter(state=0)
    data = []
    for need in needs:
        need_info = {"need_id" : need.id, "title": need.title, "description": need.description,
        "end_time": need.end_time, "field": need.field, "state": need.state, "emergency": need.emergency, "predict": need.predict,"real": need.real}
        data.append(need_info)
    
    return success_api_response({"data": data})

@response_wrapper
# @jwt_auth()
@require_POST
def edit_need(request: HttpRequest, uid: int, id: int):
    try:
        user: User = User.objects.get(id=uid)
        need: Need = Need.objects.get(id=id)
    except User.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist user")
    except Need.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-exist need")
    
    if user.state != 5:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-enterprise user")
    if need.enterprise != user:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "not the enterprise's need")
    
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "data is none")

    title = data.get('title')
    description = data.get('description')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    key_word = data.get('key_word') 
    address = data.get('address')
    
    try:
        money = int(data.get('money'))
        predict = int(data.get('predict'))
        emergency = int(data.get('emergency'))
        field = int(data.get('field'))
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "non-digit value(some digit value is wrong)")

    if title is None or description is None or money is None or start_time is None  or end_time is None or key_word is None \
        or field is None or address is None or emergency is None or predict is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid requset value")

    if not title or not description or not start_time:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "title or description or start_time cannot be empty")

    Need.objects.filter(id=id).update(title=title, description=description, money=money, 
    start_time=start_time, end_time=end_time, key_word=key_word, field=field, address=address,
    emergency=emergency, predict=predict)

    return success_api_response({})


    
