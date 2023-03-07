from rest_framework.authentication import TokenAuthentication as BaseTokenAuth
from rest_framework.exceptions import AuthenticationFailed


class TokenAuthentication(BaseTokenAuth):
    keyword = "Token"


def user_authentication_rule(user):
    if not user:
        raise AuthenticationFailed(
            "Credential(Username or Password) are incorrect, please contact support"
        )
    if not user.is_active:
        raise AuthenticationFailed("User is not active, please contact support")
    if not user.is_verified:
        raise AuthenticationFailed("User is not yet verified")
    # if user.is_disabled:
    #     raise AuthenticationFailed("User is disabled, please contact support")
    if user.is_deleted:
        raise AuthenticationFailed("User is deleted, please contact support")
    return True
