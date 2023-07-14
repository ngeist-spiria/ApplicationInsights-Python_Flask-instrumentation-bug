from django.db import models

# Create your models here.


class Post(models.Model):

    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
