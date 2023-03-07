import logging

from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler

logger = logging.getLogger("main")


def custom_exception_handler(exception, context):
    response = exception_handler(exception, context)
    message = "Response is none"
    if response is not None:
        custom_response = {
            "status_code": response.status_code,
            "result": None,
            "error": response.data,
        }
        response.data = custom_response
        message = f"data: {response.data}"
    logger.info(
        message
    ) if settings.DEBUG is False and settings.ENVIRONMENT == "PRODUCTION" else None
    return response


class NotImplementedException(ValidationError):
    def __init__(self, detail="Invalid Data", code="InvalidData", data=None):
        super(NotImplementedException, self).__init__(detail, code)
        message = f"Invalid data: {data}"
        logger.info(message)


class IncorrectDataInRequest(ValidationError):
    def __init__(self, detail="Feature not implemented", code="NotImplemented"):
        super(NotImplementedException, self).__init__(detail, code)


class ApiRequestException(ValidationError):
    def __init__(
        self,
        url=None,
        method=None,
        header=None,
        body=None,
        response=None,
        status_code=None,
        detail="Gateway Error",
        code="Gateway Error",
    ):
        super(ApiRequestException, self).__init__(detail, code)
        message = f"API_EXCEPTION  url:{url}, method:{method}, body: {body},\
             response: {response}, status_code: {status_code}"
        logger.info(message)
