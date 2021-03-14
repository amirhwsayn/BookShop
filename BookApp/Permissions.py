from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework import permissions
from .models import Token, User


class PERM_CreateUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'token' in request.headers and 'code' in request.headers:
            token = request.headers['token']
            code = request.headers['code']
            try:
                Tokencode = Token.objects.get(Token_Token=token).Token_Code
                TokenDate = Token.objects.get(Token_Token=token).Token_CreateDate
                if Tokencode == code:
                    if TokenDate + timedelta(minutes=5) > timezone.now():
                        return True
                    else:
                        return False
                else:
                    return False
            except ObjectDoesNotExist:
                return False
        else:
            return False


class PERM_User(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'token' in request.headers:
            token = request.headers['token']
            try:
                User.objects.get(User_Token=token)
                return True
            except ObjectDoesNotExist:
                return False
        else:
            return False
