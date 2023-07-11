from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



class User(User):
    description = models.CharField(
        max_length=300, blank=True, null=True, unique=False, default=""
    )
    avatar= models.FileField(upload_to='avatar', blank=True, null=True)
    phone_number = models.BigIntegerField(
        "phone number",
        blank=True,
        unique=True,
        null=True,
        validators=[MinValueValidator(1000000), MaxValueValidator(10000000000 - 1)],
    )
