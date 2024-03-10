from rest_framework import serializers

from main import models, local_messages


class LocalMessageSerializer(serializers.Serializer):
    payload = serializers.CharField(max_length=128)
    creation_time = serializers.DateTimeField(required=False)

    def create(self, validated_data: dict) -> local_messages.Message:
        payload = validated_data["payload"]
        creation_time = local_messages.creation_time_of(
            validated_data.get("creation_time"),
        )

        message = local_messages.Message(
            payload=payload,
            creation_time=creation_time,
        )

        local_messages.repository.append(message)

        return message

    def update(message: local_messages.Message, validated_data: dict) -> local_messages.Message:
        message.payload = validated_data["payload"]
        message.creation_time = local_messages.creation_time_of(
            validated_data.get("creation_time"),
        )

        return message


class OrmMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = ["payload", "creation_time"]
