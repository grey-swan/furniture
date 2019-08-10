import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *


class PrivilegeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Privilege
        fields = ('id', 'name', 'view')


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ('id', 'name', 'alias')


class RolePrivilegeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RolePrivilege
        fields = ('id', 'role', 'privilege')


class UserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRole
        fields = ('id', 'user', 'role')


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('true_name',)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    date_joined = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)
    user_role_id = serializers.ReadOnlyField(source='user_role.id')
    user_role_name = serializers.ReadOnlyField(source='user_role.role.alias')
    profile = UserProfileSerializer()  # 可以单独作为表单的一部分

    class Meta:
        model = User
        fields = ('id', 'username', 'date_joined', 'user_role_name', 'user_role_id', 'profile')

    def update(self, instance, validated_data):
        """
        更新用户，也需要重新设置密码，否则是明文
        :param instance:
        :param validated_data:
        :return:
        """
        profile_data = validated_data.pop('profile', '')
        if profile_data:
            profile = UserProfileSerializer(instance.profile, data=profile_data, partial=True)
            profile.is_valid(raise_exception=True)
            profile.save()

        return super(UserSerializer, self).update(instance, validated_data)
