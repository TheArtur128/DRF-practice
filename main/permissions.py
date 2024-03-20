from typing import Any, Callable, Optional

from django.contrib import auth
from rest_framework import permissions, views
from rest_framework.request import Request

from main import models


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: views.APIView) -> bool:
        return request.method in permissions.SAFE_METHODS


class IsForCurrentUserLazy(permissions.BasePermission):
    _get_current_user_id: Callable[[Request, views.APIView], Optional[int]]

    def has_permission(self, request: Request, view: views.APIView) -> bool:
        if not request.data:
            return True

        current_user_id = self._get_current_user_id(request, view)

        return current_user_id is None or current_user_id == request.user.id


class IsForCurrentUser(permissions.BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: views.APIView,
        obj: Any,
    ) -> bool:
        return isinstance(obj, auth.models.User) and obj.id == request.user.id


class IsMessageAuthor(permissions.BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: views.APIView,
        obj: Any,
    ) -> bool:
        return (
            isinstance(obj, models.Message)
            and obj.user is not None
            and request.user.id == obj.user.id
        )
