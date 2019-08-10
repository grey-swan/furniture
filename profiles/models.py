from django.db import models
from django.contrib.auth.models import User

from .utils import *


class Privilege(models.Model):
    """权限"""

    name = models.CharField(max_length=64, verbose_name='权限名称')
    view = models.CharField(max_length=64, verbose_name='视图')

    def __str__(self):
        return self.name


class Role(models.Model):
    """角色"""

    name = models.CharField(max_length=64, verbose_name='角色名称')
    alias = models.CharField(max_length=64, verbose_name='角色别名')
    level = models.IntegerField(verbose_name='角色级别', default=0)

    def __str__(self):
        return self.name


class RolePrivilege(models.Model):
    """角色拥有的权限"""

    role = models.ForeignKey(Role, related_name='privileges', on_delete=models.CASCADE)
    privilege = models.ForeignKey(Privilege, related_name='roles', on_delete=models.CASCADE)


class UserRole(models.Model):
    """用户角色-一对一"""

    user = models.OneToOneField(User, related_name='user_role', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, related_name='user_role', on_delete=models.CASCADE,
                             null=True, blank=True)


class UserProfile(models.Model):
    """基本用户信息"""

    true_name = models.CharField(max_length=16, verbose_name='姓名', null=True)

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
