from django.db import models


class Message(models.Model):
    payload = models.CharField(max_length=128)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __repr__(self) -> str:
        return f"Message({self.id}: {self})"

    def __str__(self) -> str:
        return f"[{self.creation_time}] {self.payload}"
