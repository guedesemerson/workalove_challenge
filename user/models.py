from django.contrib.auth.models import AbstractUser
from django.db import models


class TypeUser(models.TextChoices):
    chef = 'C', 'Chef'
    client = 'P', 'Client'


class User(AbstractUser):
    name = models.CharField(max_length=150,
                            verbose_name='Full Name')
    type_user = models.CharField(
        max_length=10,
        choices=TypeUser.choices,
        verbose_name='Type of User')

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email