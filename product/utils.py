import requests
import uuid
import ujson as json

from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from qiniu import Auth, put_data
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


WX_TOKEN_KEY = 'access_token'


def db_query(query):
    """
    查询云数据库
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


def upload_qn(filename, data):
    """
    上传七牛
    :param filename:
    :param data:
    :return:
    """
    access_key = settings.QINIU.get('ACCESS_KEY')
    secret_key = settings.QINIU.get('SECRET_KEY')
    bucket_name = settings.QINIU.get('BUCKET_NAME')

    q = Auth(access_key, secret_key)
    token = q.upload_token(bucket_name, filename)
    ret, info = put_data(token, filename, data)

    if ret['key'] == filename:
        url = ''.join(['http://hyym.oocpo.com/', filename])
    else:
        url = ''

    return url


def upload_cos(filename, data):
    """
    上传腾讯云
    :param filename:
    :param data:
    :return:
    """
    secret_id = settings.TX_COS.get('SECRET_ID')
    secret_key = settings.TX_COS.get('SECRET_KEY')
    region = settings.TX_COS.get('REGION')
    bucket_name = settings.TX_COS.get('BUCKET_NAME')

    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
    client = CosS3Client(config)

    response = client.put_object(
        Bucket=bucket_name,
        Body=data,
        Key=filename,
        EnableMD5=False
    )

    # e_tag = response['ETag']
    url = 'https://{bucket}.cos.{region}.myqcloud.com/{filename}'.format(
        bucket=bucket_name, region=region, filename=filename
    )
    return url
