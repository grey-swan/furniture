from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'privileges', views.PrivilegeViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'role_privileges', views.RolePrivilegeViewSet)
router.register(r'user_role', views.UserRoleViewSet)

app_name = 'profiles'
urlpatterns = [
    path(r'', include(router.urls)),
    path('', views.AdminIndex.as_view(), name='admin_index'),
]
