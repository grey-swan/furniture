from __future__ import absolute_import, unicode_literals
import requests

from django.conf import settings
from django.core.cache import cache
from celery import shared_task

from .utils import WX_TOKEN_KEY


@shared_task
def task_deal_access_token():
    """刷新微信access_token"""
    print('start set access_token')

    key = WX_TOKEN_KEY
    app_id = settings.WECHAT.get('APPID', '')
    app_secret = settings.WECHAT.get('APPSECRET', '')

    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'

    resp = requests.get(url % (app_id, app_secret)).json()
    cache.set(key, resp.get(key), 7200)
    print('set access_token success')
