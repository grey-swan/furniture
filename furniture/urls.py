"""furniture URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, include
from profiles.views import AdminIndex

urlpatterns = [
    path('api/profiles/', include('profiles.urls', namespace='prof')),
    path('api/product/', include('product.urls', namespace='prod')),
    path('', AdminIndex.as_view(), name='admin_index'),
]


if settings.DEBUG:
    urlpatterns += [
        # 开启rest_framework登陆界面
        path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    ]
