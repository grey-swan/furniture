import datetime

from rest_framework.authentication import TokenAuthentication, SessionAuthentication, exceptions
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .utils import EXPIRED_TIME


class TokenAuth(TokenAuthentication):
    def authenticate(self, request):
        ret = super(TokenAuth, self).authenticate(request)
        # 如果前端没有传Token则报错
        if not ret:
            raise exceptions.AuthenticationFailed(_('Token不存在，请重新登录'))

        return ret

    def authenticate_credentials(self, key):
        user, token = super(TokenAuth, self).authenticate_credentials(key)

        # 设置token失效时间
        if timezone.now() > (token.created + datetime.timedelta(**EXPIRED_TIME)):
            raise exceptions.AuthenticationFailed(_('Token已过期，请重新登录'))

        return user, token


class SessionAuth(SessionAuthentication):
    def authenticate(self, request):
        ret = super(SessionAuth, self).authenticate(request)
        if not ret:
            raise exceptions.AuthenticationFailed(_('Session已过期或不存在，请重新登录'))

        return ret