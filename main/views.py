from functools import partial
from typing import Optional, TYPE_CHECKING

from django.contrib import auth
from django.http import Http404, HttpRequest
from rest_framework import decorators, parsers, status, generics, viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from main import serializers, local_messages, models, permissions


@decorators.api_view(['GET', 'POST'])
def local_message_list_view(
    request: Request,
    format: Optional[str] = None,
) -> Response:
    if request.method == 'GET':
        serializer = serializers.LocalMessageSerializer.many_init(
            local_messages.repository.get_all(),
        )

        return Response(serializer.data)

    data = parsers.JSONParser().parse(request)
    serializer = serializers.LocalMessageSerializer(data=data, many=True)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocalMessageView(APIView):
    def get(
        self,
        request: Request,
        id: int,
        format: Optional[str] = None,
    ) -> Response:
        serializer = serializers.LocalMessageSerializer(self.__get_message(id))

        return Response(serializer.data)

    def put(
        self,
        request: Request,
        id: int,
        format: Optional[str] = None,
    ) -> Response:
        message = self.__get_message(id)

        data = parsers.JSONParser().parse(request)
        serializer = serializers.LocalMessageSerializer(message, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(dict(), status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(
        self,
        request: Request,
        id: int,
        format: Optional[str] = None,
    ) -> Response:
        local_messages.repository.remove_by_id(id)

        return Response(dict(), status=status.HTTP_204_NO_CONTENT)

    def __get_message(self, id: int) -> local_messages.Message:
        message = local_messages.repository.get_by_id(id)

        if message is None:
            raise Http404(f"Message with id {id} does not exist")

        return message


if TYPE_CHECKING:
    _GenericAPIView = generics.GenericAPIView[models.Message]
else:
    _GenericAPIView = generics.GenericAPIView 


class OrmMessageListView(
    _GenericAPIView,
    ListModelMixin,
    CreateModelMixin,
):
    class _IsMessageAuthorLazy(permissions.IsForCurrentUserLazy):
        def _get_current_user_id(
            self,
            request: Request,
            view: APIView,
        ) -> Optional[int]:
            current_user_id = request.data.get("author_id", None)

            try:
                return int(current_user_id)
            except ValueError:
                return None

    queryset = models.Message.objects.all().order_by("-creation_time")
    serializer_class = serializers.OrmMessageSerializer
    permission_classes = [permissions.ReadOnly | _IsMessageAuthorLazy]

    def get(self, request: Request) -> Response:
        return self.list(request)

    def post(self, request: Request) -> Response:
        return self.create(request)


if TYPE_CHECKING:
    _RetrieveAPIView = generics.RetrieveAPIView[models.Message]
    _UpdateAPIView = generics.UpdateAPIView[models.Message]
    _DestroyAPIView = generics.DestroyAPIView[models.Message]
else:
    _RetrieveAPIView = generics.RetrieveAPIView
    _UpdateAPIView = generics.UpdateAPIView
    _DestroyAPIView = generics.DestroyAPIView


class OrmMessageView(_RetrieveAPIView, _UpdateAPIView, _DestroyAPIView):
    serializer_class = serializers.OrmMessageSerializer
    permission_classes = [permissions.ReadOnly | permissions.IsMessageAuthor]

    __message_id: Optional[int] = None

    def setup(
        self,
        request: HttpRequest,
        id: int,
        format: Optional[str] = None,
    ) -> None:
        super().setup(request, id, format)
        self.__message_id = id

    def get_object(self) -> models.Message:
        assert self.__message_id is not None

        return generics.get_object_or_404(
            models.Message.objects,
            id=self.__message_id,
        )


if TYPE_CHECKING:
    _ListAPIView = generics.ListAPIView[auth.models.User]
else:
    _ListAPIView = generics.ListAPIView


class UserListView(_ListAPIView):
    queryset = auth.models.User.objects.all()
    serializer_class = serializers.UserSerializer


if TYPE_CHECKING:
    _UserView_RetrieveAPIView = generics.RetrieveAPIView[auth.models.User]
else:
    _UserView_RetrieveAPIView = generics.RetrieveAPIView


class UserView(_UserView_RetrieveAPIView):
    queryset = auth.models.User.objects.all()
    serializer_class = serializers.UserSerializer


@decorators.api_view(["GET"])
def root_view(request: Request, format: Optional[str] = None) -> Response:
    reverse_ = partial(reverse, request=request, format=format)

    return Response({
        'temporary-messages': reverse_('main:temporary-messages'),
        'temporary-message': reverse_('main:temporary-message', ['0']),
        'long-term-messages': reverse_('main:long-term-messages'),
        'long-term-message': reverse_('main:long-term-message', ['0']),
        'users': reverse_('main:users'),
        'user': reverse_('main:user', ['0']),
        'read-only-users': reverse_('main:read-only-users'),
        'profiles': reverse_('main:profiles'),
        'profile': reverse_('main:profile', ['0']),
    })


if TYPE_CHECKING:
    _AReadOnlyModelViewSet = viewsets.ReadOnlyModelViewSet[auth.models.User]
else:
    _AReadOnlyModelViewSet = viewsets.ReadOnlyModelViewSet


class ReadOnlyUserViewSet(_AReadOnlyModelViewSet):
    queryset = auth.models.User.objects.all()
    serializer_class = serializers.UserSerializer


if TYPE_CHECKING:
    _AModelViewSet = viewsets.ModelViewSet[auth.models.User]
else:
    _AModelViewSet = viewsets.ModelViewSet


class ProfileViewSet(_AModelViewSet):
    queryset = auth.models.User.objects.all()
    serializer_class = serializers.ProfileSerializer

    lookup_field = 'id'

    permission_classes = [permissions.ReadOnly | permissions.IsForCurrentUser]
