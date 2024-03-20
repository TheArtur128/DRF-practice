from typing import Callable, TypeAlias

from django.http import HttpRequest, HttpResponse
from django.conf import settings


_Handler: TypeAlias = Callable[[HttpRequest], HttpResponse]


def default_header_settings_middleware(get_response: _Handler) -> _Handler:
    def handle(request: HttpRequest) -> HttpResponse:
        request.META.update(settings.DEFAULT_HEADERS)

        return get_response(request)

    return handle
