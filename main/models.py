from django.db import models
from django.contrib import auth


class Message(models.Model):
    user = models.ForeignKey(
        auth.models.User,
        on_delete=models.CASCADE,
        related_name="messages",
        default=None,
        null=True,
        blank=True,
    )
    payload = models.CharField(max_length=128)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __repr__(self) -> str:
        return f"Message({self.id}: {self})"

    def __str__(self) -> str:
        return f"[{self.creation_time}] {self.payload}"
