import uuid

from django.http import JsonResponse
from django.conf import settings
from rest_framework import views

from .serializer import *
from .utils import upload_qn
from . import mviewsets
from profiles import AuthLogin
from profiles.views import LargePageNumberPagination


class CategoryViewSet(mviewsets.MyModelViewSet):
    collection_name = 'category'
    serializer_class = CategorySerializer
    pagination_class = LargePageNumberPagination
    authentication_classes = (AuthLogin,)


class StyleViewSet(mviewsets.MyModelViewSet):
    collection_name = 'style'
    serializer_class = StyleSerializer
    pagination_class = LargePageNumberPagination
    authentication_classes = (AuthLogin,)


class FurnitureViewSet(mviewsets.MyModelViewSet):
    collection_name = 'furniture'
    serializer_class = FurnitureSerializer
    authentication_classes = (AuthLogin,)


class CaseViewSet(mviewsets.MyModelViewSet):
    collection_name = 'case'
    serializer_class = CaseSerializer
    authentication_classes = (AuthLogin,)


class SoftViewSet(mviewsets.MyModelViewSet):
    collection_name = 'soft'
    serializer_class = SoftSerializer
    authentication_classes = (AuthLogin,)


class DesignerViewSet(mviewsets.MyModelViewSet):
    collection_name = 'designer'
    serializer_class = DesignerSerializer
    authentication_classes = (AuthLogin,)


class CompanyViewSet(mviewsets.MyModelViewSet):
    collection_name = 'company'
    serializer_class = CompanySerializer
    authentication_classes = (AuthLogin,)


class BannerViewSet(mviewsets.MyModelViewSet):
    collection_name = 'banner'
    serializer_class = BannerSerializer
    authentication_classes = (AuthLogin,)


class OrderViewSet(mviewsets.MyModelViewSet):
    collection_name = 'order'
    serializer_class = OrderSerializer
    authentication_classes = (AuthLogin,)


class ImgUpload(views.APIView):
    """图片上传"""
    authentication_classes = (AuthLogin,)

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

    # def post(self, request):
    #     result = {'errno': 1, 'data': []}
    #
    #     file_items = self.request.FILES.lists()
    #     # 上传文件
    #     if file_items:
    #         for file_item in file_items:
    #             item = file_item[1]
    #             file_name = item[0].name
    #
    #             prefix = file_name[file_name.rfind('.'):]  # 后缀
    #             filename = ''.join([uuid.uuid1().hex, prefix])
    #
    #             data = b''.join([chunk for chunk in item[0].chunks()])
    #             img_url = upload_qn(filename, data)
    #             result['data'].append(img_url)
    #
    #         result['errno'] = 0
    #
    #     return JsonResponse(result)

    # def post(self, request):
    #     result = {'errno': 1, 'data': []}
    #
    #     file_items = self.request.FILES.lists()
    #     # 上传文件
    #     if file_items:
    #         for file_item in file_items:
    #             item = file_item[1]
    #             file_name = item[0].name
    #
    #             prefix = file_name[file_name.rfind('.'):]  # 后缀
    #             filename = ''.join([uuid.uuid1().hex, prefix])
    #             data = b''.join([chunk for chunk in item[0].chunks()])
    #             img_url = upload_cos(filename, data)
    #             result['data'].append(img_url)
    #
    #         result['errno'] = 0
    #
    #     return JsonResponse(result)
