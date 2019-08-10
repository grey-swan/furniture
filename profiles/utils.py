import functools
import datetime
import requests
import io
import uuid

from rest_framework.response import Response
from django.shortcuts import redirect
from django.utils import timezone
from django.conf import settings
from wechatpy.oauth import WeChatOAuth
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import WeChatClient, parse_message, create_reply


EXPIRED_TIME = {'days': 30}  # token过期时间 'seconds': 10

ROLE_SUPER = 'super'
ROLE_ANYONE = 'anyone'


def decode_params(string):
    """
    格式查询参数
    :param string:
    :return:
    """
    params = string.split('&')
    data = [param.split('=') for param in params if param]

    return dict(data)
