from .models import Student, Teacher, User
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import PermissionDenied

class AccountSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'id', 'password', 'name', 'role', 'is_staff']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data['role']=None
        validated_data.pop('role')      # so that role can not be assigned during sign-up
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
