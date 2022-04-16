from django.http import HttpRequest
from core.api.utils import (ErrorCode, success_api_response, failed_api_response, wrapped_api, response_wrapper)
from core.api.auth import jwt_auth
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from core.models.id import ID
from core.models.user import User
import json


@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def create_id_image(request: HttpRequest):
    """
    :param request:
        FILES: image: new image
    :return:
    """
    image_file = request.FILES.get("id", None)
    #current_user = request.user
    current_user = User.objects.get(id=1)
    if image_file is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "id has not provided.")

    id = ID()
    id.created_by = current_user
    id.file = image_file

    try:
        id.save()
    except Exception:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "add id error.")

    return success_api_response({
        "message": "success add a id."
    })