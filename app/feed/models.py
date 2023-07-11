from django.db import models
from user.models import User
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField


class Post(models.Model):
    title = models.CharField(
        max_length=300, blank=False, null=False, unique=False, default=""
    )
    description = models.CharField(
        max_length=300, blank=True, null=True, unique=False, default=""
    )
    platform = models.CharField(
        max_length=300, blank=False, null=False, unique=False, default=""
    )
    link = models.CharField(
        max_length=300, blank=False, null=False, unique=False, default=""
    )
    post_link = models.URLField(
        max_length=300, blank=False, null=False, unique=False, default=""
    )
    image = models.FileField(upload_to="posts", default="../static/default_post_image.png", blank=True, unique=False)
    is_private = models.BooleanField(null=True, blank=True, default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User,
        related_name="own_posts",
        null=True,
        unique=False,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.title