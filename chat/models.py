from django.db import models


# Create your models here.
class ChatSystem(models.Model):
    name = models.CharField(
        max_length=256, error_messages={"unique": "Diese Gruppe existiert bereits."}
    )
    system_setup_text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
