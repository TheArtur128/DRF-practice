from django.http import Http404

from rest_framework import decorators, parsers, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from main import serializers, local_messages


@decorators.api_view(['GET', 'POST'])
def local_message_list(request: Request, format=None) -> Response:
    if request.method == 'GET':
        serializer = serializers.LocalMessageSerializer(
            local_messages.repository.get_all(),
            many=True,
        )

        return Response(serializer.data)

    elif request.method == 'POST':
        data = parsers.JSONParser().parse(request)
        serializer = serializers.LocalMessageSerializer(data=data, many=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@(lambda cls: cls.as_view())
class local_message(APIView):
    def get(self, request: Request, id: int, format=None) -> Response:
        serializer = serializers.LocalMessageSerializer(self.__get_message(id))

        return Response(serializer.data)

    def put(self, request: Request, id: int, format=None) -> Response:
        message = self.__get_message(id)

        data = parsers.JSONParser().parse(request)
        serializer = serializers.LocalMessageSerializer(message, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(dict(), status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, id: int, format=None) -> Response:
        local_messages.repository.remove_by_id(id)

        return Response(dict(), status=status.HTTP_204_NO_CONTENT)

    def __get_message(self, id: int) -> local_messages.Message:
        message = local_messages.repository.get_by_id(id)

        if message is None:
            raise Http404(f"Message with id {id} does not exist")

        return message
