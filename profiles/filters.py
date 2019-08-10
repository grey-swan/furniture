from django.db.models import Q
from django_filters import rest_framework as filters

from .models import User


class UserFilter(filters.FilterSet):
    role = filters.CharFilter(field_name='user_role__role__alias', lookup_expr='exact')

    class Meta:
        model = User
        fields = ['role']

    @property
    def qs(self):
        """重写ps可以获取request对象"""
        queryset = super(UserFilter, self).qs
        name = self.request.query_params.get('name', '')
        if name:
            return queryset.filter(Q(profile__true_name__icontains=name) |
                                   Q(wechat__nickname__icontains=name))
        else:
            return queryset
