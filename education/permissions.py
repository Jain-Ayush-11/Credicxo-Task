# to define custom permission classes
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        return False

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='Students'):
            return True
        return False


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.groups)
        if request.user is not None and request.user.groups.filter(name='Teachers'):
            return True
        return False