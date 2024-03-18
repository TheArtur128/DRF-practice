from typing import Any

from rest_framework import permissions, views
from rest_framework.request import Request

from main import models


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: views.APIView) -> bool:
        return request.method in permissions.SAFE_METHODS


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
