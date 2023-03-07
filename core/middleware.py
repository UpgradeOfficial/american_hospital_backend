import json
import logging
import uuid

from django.conf import settings
from django.http.response import Http404

logger = logging.getLogger("main")


class RequestHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if f"/{settings.BACKEND_ADMIN_URL}" not in request.path:
            if request.path not in [
                "/",
                "/swagger",
                "/swagger/",
                "/schema/",
                "/__debug__/history_sidebar/",
                "/favicon.ico",
            ]:
                platform_key = request.headers.get("x-api-key")
                if not platform_key or platform_key != settings.PLATFORM_KEY:
                    return Http404

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"

        return response


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        user = request.user
        requestId = str(uuid.uuid4())
        request.id = requestId
        user_login_token = user.user_login_token if user.is_authenticated else ""
        logger.info(
            "ACCESS_REQUEST: "
            + json.dumps(
                {
                    "requestId": requestId,
                    "user_login_token": user_login_token,
                    "url": request.path,
                    "method": request.method,
                    "headers": request.headers.__dict__,
                }
            )
        )
        try:
            response = self.get_response(request)
        except Exception as e:
            logger.info(
                "ACCESS_EXCEPTION: "
                + json.dumps({"message": e.get_message(), "requestId": requestId})
            )
            raise e
        logger.info(
            "ACCESS_RESPONSE: "
            + json.dumps({"status": response.status_code, "requestId": requestId})
        )
        response.headers["X-REQUEST-ID"] = requestId
        return response
