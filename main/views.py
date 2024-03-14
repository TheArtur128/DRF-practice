from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import parsers, status

from main import serializers, local_messages


@csrf_exempt
def local_message_list(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        serializer = serializers.LocalMessageSerializer(
            local_messages.repository.get_all(),
            many=True,
        )

        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = parsers.JSONParser().parse(request)
        serializer = serializers.LocalMessageSerializer(data=data, many=True)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(
                serializer.data,
                status=status.HTTP_201_CREATED,
                safe=False,
            )

        return JsonResponse(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
            safe=False,
        )


@csrf_exempt
def local_message(request: HttpRequest, id: int) -> JsonResponse:
    message = local_messages.repository.get_by_id(id)

    if message is None:
        return JsonResponse(dict(), status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = serializers.LocalMessageSerializer(message)

        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = parsers.JSONParser().parse(request)
        serializer = serializers.LocalMessageSerializer(message, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(dict(), status=status.HTTP_204_NO_CONTENT)

        return JsonResponse(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
            safe=False,
        )

    elif request.method == 'DELETE':
        local_messages.repository.remove_by_id(id)
        return JsonResponse(dict(), status=status.HTTP_204_NO_CONTENT)
