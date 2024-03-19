from typing import TypedDict

from django.contrib import auth
from rest_framework import serializers

from main import models, local_messages


class LocalMessageSerializer(serializers.Serializer[local_messages.Message]):
    class _DataToWrite(TypedDict):
        payload: str

    id = serializers.IntegerField(read_only=True)
    payload = serializers.CharField(max_length=128)
    creation_time = serializers.DateTimeField(read_only=True)

    __repository: local_messages.Repository = local_messages.repository

    def create(self, validated_data: _DataToWrite) -> local_messages.Message:
        message = local_messages.Message(payload=validated_data["payload"])
        self.__repository.save(message)

        return message

    def update(
        self,
        message: local_messages.Message,
        validated_data: _DataToWrite,
    ) -> local_messages.Message:
        message.payload = validated_data["payload"]

        return message


class OrmMessageSerializer(serializers.ModelSerializer[models.Message]):
    class Meta:
        model = models.Message
        fields = ["id", "author_id", "payload", "creation_time"]

    class _User(TypedDict):
        id: int

    class _DataToWrite(TypedDict):
        user: "OrmMessageSerializer._User"
        payload: str

    creation_time = serializers.DateTimeField(read_only=True)
    author_id = serializers.IntegerField(source="user.id", allow_null=True)

    def create(self, validated_data: _DataToWrite) -> models.Message:
        return models.Message.objects.create(
            user_id=validated_data["user"]["id"],
            payload=validated_data["payload"],
        )


class UserSerializer(serializers.ModelSerializer[auth.models.User]):
    class Meta:
        model = auth.models.User
        fields = ["id", "username", "messages"]

    messages = OrmMessageSerializer(many=True, read_only=True)
