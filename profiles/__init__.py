from django.conf import settings

if settings.DEBUG_ME in (0, 1):
    from .authenications import TokenAuth as AuthLogin
else:
    from .authenications import SessionAuth as AuthLogin
