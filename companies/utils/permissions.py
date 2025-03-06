from rest_framework import permissions

from django.contrib.auth.models import Permission

def check_permission(user, method, permission_to):

    if not user.is_authenticated:
        return False
    print(user.is_owner)
    if user.is_owner:
        return True
    
    required_permission = "view_"+permission_to

    if method == "POST":
        required_permission = "add_"+permission_to
    elif method == "PUT":
        required_permission = "change_"+permission_to
    elif method == "DELETE":
        required_permission = "delete_"+permission_to
    
    groupings = user.grouping_set.all()

    for group in groupings:
        permissions = group.permissions.all()
        for permission in permissions:
            if permission.codename == required_permission:
                return True

class EmployeePermissions(permissions.BasePermission):
    message = "O usuário não tem permissão para gerenciar funcionários"

    def has_permission(self, request, view):
        return check_permission(request.user, request.method, "employee")

class GroupingPermissions(permissions.BasePermission):
    message = "O usuário não tem permissão para gerenciar grupos"

    def has_permission(self, request, view):
        return check_permission(request.user, request.method, "grouping")

class PermissionPermissions(permissions.BasePermission):
    message = "O usuário não tem permissão para gerenciar permissões"

    def has_permission(self, request, view):
        return check_permission(request.user, request.method, "permission")

class TaskPermissions(permissions.BasePermission):
    message = "O usuário não tem permissão para gerenciar tarefas"

    def has_permission(self, request, view):
        return check_permission(request.user, request.method, "task")
