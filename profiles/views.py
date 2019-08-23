from rest_framework import views
from rest_framework.pagination import PageNumberPagination, OrderedDict
from rest_framework.viewsets import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.renderers import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.http import HttpResponse
from django.db.models import Sum, Avg
from django_filters import rest_framework as filters

from . import mviewsets
from . import AuthLogin
from .serializer import *
from .permissions import *
from .utils import *
from .filters import *


class SmallPageNumberPagination(PageNumberPagination):
    page_size = 16
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        prev_page, next_page = None, None
        if self.page.has_previous():
            prev_page = self.page.previous_page_number()
        if self.page.has_next():
            next_page = self.page.next_page_number()

        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page', self.page.number),
            ('num_pages', self.page.paginator.num_pages),
            ('per_page', self.page.paginator.per_page),
            ('previous', prev_page),
            ('next', next_page),
            ('data', data)
        ]))


class LargePageNumberPagination(SmallPageNumberPagination):
    page_size = 128


class UserViewSet(mviewsets.MyEditScanModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowRole, EditIsOwner)
    authentication_classes = (AuthLogin,)
    pagination_class = SmallPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter

    @action(detail=False, methods=['post'], authentication_classes=[],
            permission_classes=[])
    def login(self, request, *args, **kwargs):
        """自定义登陆方法"""
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        data = {'username': username, 'password': password}
        serializer = AuthTokenSerializer(data=data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as exc:
            raise ValidationError('用户名或密码错误')

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        if timezone.now() > (token.created + datetime.timedelta(**EXPIRED_TIME)):
            # 过期的token删除后重新创建
            user.auth_token.delete()
            token, created = Token.objects.get_or_create(user=user)

        response = Response(data={'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)

        return response

    @action(detail=True, methods=['post'], authentication_classes=[AuthLogin],
            permission_classes=[UserIsSelf])
    def logout(self, request, pk=None):
        """自定义注销方法"""
        user = self.get_object()
        Token.objects.filter(user=user).delete()

        return Response(status=status.HTTP_200_OK)


class PrivilegeViewSet(mviewsets.MyModelViewSet):
    queryset = Privilege.objects.all()
    serializer_class = PrivilegeSerializer
    permission_classes = (IsSuper,)
    authentication_classes = (AuthLogin,)
    pagination_class = SmallPageNumberPagination


class RoleViewSet(mviewsets.MyModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (IsSuper,)
    authentication_classes = (AuthLogin,)
    pagination_class = SmallPageNumberPagination

    def get_queryset(self):
        queryset = super(RoleViewSet, self).get_queryset()
        level = self.request.user.user_role.role.level
        queryset = queryset.filter(level__lt=level)
        return queryset


class RolePrivilegeViewSet(mviewsets.MyModelViewSet):
    queryset = RolePrivilege.objects.all()
    serializer_class = RolePrivilegeSerializer
    permission_classes = (IsSuper,)
    authentication_classes = (AuthLogin,)
    pagination_class = SmallPageNumberPagination


class UserRoleViewSet(mviewsets.MyEditScanModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = (IsAdmin,)
    authentication_classes = (AuthLogin,)

    def perform_update(self, serializer):
        user = serializer.validated_data.get('user')
        if self.request.user == user:
            raise ValidationError('不能审核自己')

        super(UserRoleViewSet, self).perform_update(serializer)


class AdminIndex(views.APIView):

    def get(self, request):
        """后台管理系统重定向到首页"""
        return redirect('/index.html#/')
