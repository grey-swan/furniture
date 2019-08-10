import ujson as json
import uuid

from django.http import JsonResponse
from django.conf import settings
from rest_framework import views, viewsets
from rest_framework.pagination import PageNumberPagination, OrderedDict
from rest_framework.viewsets import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.renderers import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.http import HttpResponse
from django.db.models import Sum, Avg
from django_filters import rest_framework as filters

from .serializer import *
from . import mviewsets
from profiles.views import LargePageNumberPagination, SmallPageNumberPagination


class CategoryViewSet(mviewsets.MyModelViewSet):
    collection_name = 'category'
    serializer_class = CategorySerializer
    pagination_class = LargePageNumberPagination


class StyleViewSet(mviewsets.MyModelViewSet):
    collection_name = 'style'
    serializer_class = StyleSerializer
    pagination_class = LargePageNumberPagination


class FurnitureViewSet(mviewsets.MyModelViewSet):
    collection_name = 'furniture'
    serializer_class = FurnitureSerializer
    pagination_class = SmallPageNumberPagination


class CaseViewSet(mviewsets.MyModelViewSet):
    collection_name = 'case'
    serializer_class = CaseSerializer
    pagination_class = SmallPageNumberPagination


class SoftViewSet(mviewsets.MyModelViewSet):
    collection_name = 'soft'
    serializer_class = SoftSerializer
    pagination_class = SmallPageNumberPagination


class DesignerViewSet(mviewsets.MyModelViewSet):
    collection_name = 'designer'
    serializer_class = DesignerSerializer
    pagination_class = SmallPageNumberPagination


class CompanyViewSet(mviewsets.MyModelViewSet):
    collection_name = 'company'
    serializer_class = CompanySerializer
    pagination_class = SmallPageNumberPagination


class BannerViewSet(mviewsets.MyModelViewSet):
    collection_name = 'banner'
    serializer_class = BannerSerializer
    pagination_class = SmallPageNumberPagination


class OrderViewSet(mviewsets.MyModelViewSet):
    collection_name = 'order'
    serializer_class = OrderSerializer
    pagination_class = SmallPageNumberPagination


class ImgUpload(views.APIView):
    """图片上传"""

    def post(self, request):
        result = {'errno': 1, 'data': []}

        file_items = request.FILES.lists()
        # 上传文件
        if file_items:
            for file_item in file_items:

                file_name, item = file_item
                prefix = file_name[file_name.rfind('.'):]  # 后缀
                filename = ''.join([uuid.uuid1().hex, prefix])

                save_path = '%s/%s' % (settings.MEDIA_ROOT, filename)
                resp_path = '%s/media/img/%s' % (settings.DOMAIN, filename)
                with open(save_path, 'wb') as f:
                    for chunk in item[0].chunks():
                        f.write(chunk)

                result['data'].append(resp_path)

            result['errno'] = 0

        return JsonResponse(result)
