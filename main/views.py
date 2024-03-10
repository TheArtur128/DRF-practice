from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import parsers

from main import serializers, local_messages


@csrf_exempt
def local_message_list(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        serializer = serializers.LocalMessageSerializer(
            local_messages.repository,
            many=True,
        )

        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = parsers.JSONParser.parse(request)
        serializer = serializers.LocalMessageSerializer(data=data, many=True)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)
