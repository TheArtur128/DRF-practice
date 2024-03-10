from django.db import models


class Message(models.Model):
    payload = models.CharField(max_length=128)
    creation_time = models.DateTimeField(auto_now_add=True)
