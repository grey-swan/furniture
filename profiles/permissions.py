from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission, DjangoModelPermissions, SAFE_METHODS
from profiles.models import Role, Privilege, RolePrivilege, UserRole

ADMIN_USER = ('super', 'staff')
EDIT_ACTION = ('create', 'update', 'partial_update', 'destroy')


class AuthPermission(BasePermission):
    """登陆验证，子类只需要super调用has_permission即可，has_object_permission不需要"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise ValidationError('请登录')
        return True


class IsSuper(AuthPermission):
    """只有超级管理员才能查看和修改资源，普通员工无权限"""

    def has_permission(self, request, view):
        super(IsSuper, self).has_permission(request, view)

        user = request.user
        if not UserRole.objects.filter(role__alias='super', user=user).exists():
            return False
        return True


class IsAdmin(AuthPermission):
    """角色为超级管理员或律品员工"""

    def has_permission(self, request, view):
        super(IsAdmin, self).has_permission(request, view)

        user = request.user
        if not UserRole.objects.filter(role__alias__in=ADMIN_USER, user=user).exists():
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not UserRole.objects.filter(role__alias__in=ADMIN_USER, user=user).exists():
            return False
        return True


class UserIsSelf(IsAdmin):
    """对于非管理员用户，资源属于自己就可以访问--只针对user表"""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user == obj:
            return True

        return super(UserIsSelf, self).has_object_permission(request, view, obj)


class EditUserIsSelf(AuthPermission):
    """只能更新自己的数据"""

    def has_object_permission(self, request, view, obj):
        """只能更新自己的数据"""
        if view.action.lower() in EDIT_ACTION and request.user != obj:
            return False

        return True


class EditIsAdmin(AuthPermission):
    """只有管理员能编辑"""

    def has_permission(self, request, view):
        super(EditIsAdmin, self).has_permission(request, view)

        user_role = request.user.user_role.role.alias
        if view.action and view.action.lower() in EDIT_ACTION:
            return True if user_role in ADMIN_USER else False

        return True

    def has_object_permission(self, request, view, obj):
        user_role = request.user.user_role.role.alias
        if view.action.lower() in EDIT_ACTION:
            return True if user_role in ADMIN_USER else False

        return True


class EditIsOwner(IsAdmin):
    """只能更新自己的数据"""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        """针对和User表有关联的模型，且关联字段名为user。管理员有权限更新"""
        flag = super(EditIsOwner, self).has_object_permission(request, view, obj)
        if flag:
            return True

        if view.action.lower() in EDIT_ACTION and request.user != obj.user:
            return False

        return True


class AllowRole(AuthPermission):
    """必须有指定角色才能访问特定视图"""

    def has_permission(self, request, view):
        super(AllowRole, self).has_permission(request, view)

        view_name = request.resolver_match.view_name
        user = request.user

        privileges = Privilege.objects.filter(roles__role__user_role__user=user)
        ps = [p.view for p in privileges]

        return True if view_name in set(ps) else False
