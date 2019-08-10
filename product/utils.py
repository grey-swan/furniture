import requests
import ujson as json

from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import ValidationError


WX_TOKEN_KEY = 'access_token'


def db_query2(method, query):
    """
    查询云数据库
    :param method:
    :param query:
    :return:
    """
    methods = {
        'get': 'databasequery',
        'add': 'databaseadd',
        'update': 'databaseupdate',
        'delete': 'databasedelete'
    }
    m = methods.get(method)
    if not m:
        return []

    try:
        access_token = cache.get(WX_TOKEN_KEY, '')
        if not access_token:
            # deal_access_token()
            # access_token = cache.get(WX_TOKEN_KEY, '')
            raise ValidationError('access token is not exist')

        url = 'https://api.weixin.qq.com/tcb/%s?access_token=%s' % (m, access_token)
        data = {
            'env': settings.WECHAT.get('ENV'),
            'query': query
        }
        print(query)

        resp = requests.post(url=url, json=data).json()
        if resp.get('errcode') == 0:
            queryset =  [json.loads(d) for d in resp.get('data', ['[]'])]
        else:
            raise Exception(resp.get('errmsg', ''))
    except Exception as exc:
        print('cloud error: ', exc)
        raise ValidationError(exc)

    return queryset


def db_query(query):
    """
    查询云数据库
    :param method:
    :param query:
    :return:
    """
    cloud_fun_name = 'databaseOper'

    try:
        access_token = cache.get(WX_TOKEN_KEY, '')
        if not access_token:
            raise ValidationError('access token is not exist')

        env = settings.WECHAT.get('ENV')
        url = 'https://api.weixin.qq.com/tcb/invokecloudfunction?access_token=%s&env=%s&name=%s' % \
              (access_token, env, cloud_fun_name)

        resp = requests.post(url=url, json=query).json()
        if resp.get('errcode') == 0:
            queryset = json.loads(resp.get('resp_data', {}))
            queryset = queryset.get('data', [])
        else:
            raise Exception(resp.get('errmsg', ''))
    except Exception as exc:
        print('cloud error: ', exc)
        raise ValidationError(exc)

    return queryset
