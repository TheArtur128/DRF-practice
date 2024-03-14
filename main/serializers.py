from rest_framework import serializers

from main import models, local_messages


class LocalMessageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    payload = serializers.CharField(max_length=128)
    creation_time = serializers.DateTimeField(required=False, read_only=True)

    __repository: local_messages.Repository = local_messages.repository

    def create(self, validated_data: dict) -> local_messages.Message:
        message = local_messages.Message(payload=validated_data["payload"])
        self.__repository.save(message)

        return message

    def update(self, message: local_messages.Message, validated_data: dict) -> local_messages.Message:
        message.payload = validated_data["payload"]

        return message


class OrmMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = ["payload", "creation_time"]
