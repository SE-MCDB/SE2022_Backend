from django.http import HttpRequest
from core.api.utils import (ErrorCode, success_api_response, failed_api_response, wrapped_api, response_wrapper)
from core.api.auth import jwt_auth
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from core.models.license import License
from core.models.user import User
import json


@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def create_license_image(request: HttpRequest):
    """
    :param request:
        FILES: image: new image
    :return:
    """
    image_file = request.FILES.get("license", None)
    #current_user = request.user
    current_user = User.objects.get(id=1)
    if image_file is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "license has not provided.")

    license = License()
    license.created_by = current_user
    license.file = image_file

    try:
        license.save()
    except Exception:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "add license error.")

    return success_api_response({
        "message": "success add a license."
    })