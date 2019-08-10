from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewSet, base_name='category')
router.register(r'style', views.StyleViewSet, base_name='style')
router.register(r'furniture', views.FurnitureViewSet, base_name='furniture')
router.register(r'case', views.CaseViewSet, base_name='case')
router.register(r'soft', views.SoftViewSet, base_name='soft')
router.register(r'designer', views.DesignerViewSet, base_name='designer')
router.register(r'company', views.CompanyViewSet, base_name='company')
router.register(r'banner', views.BannerViewSet, base_name='banner')
router.register(r'order', views.OrderViewSet, base_name='order')

app_name = 'product'
urlpatterns = [
    path(r'', include(router.urls)),
    path(r'img/upload/', views.ImgUpload.as_view(), name='img-upload'),
]
