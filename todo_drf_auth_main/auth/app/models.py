from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

user_model = settings.AUTH_USER_MODEL


class User(AbstractUser):
    username = models.CharField(
        verbose_name="Username",
        max_length=300,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
    )
    last_pwd_update = models.DateTimeField(
        verbose_name="Last update password", auto_now_add=True
    )
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    age= models.IntegerField(default=0, null=True)
    desc = models.CharField(max_length=255, null=True)
    email = models.EmailField(verbose_name="Email", db_index=True, unique=True)
    is_verified = models.BooleanField(verbose_name="Is verified", default=False)


class Skill(models.Model):
    class Meta:
        verbose_name = "Скилзы"

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="skills",
    )
    name = models.CharField(max_length=255, default=None, null=True)
    value = models.IntegerField(default=0)


class Work(models.Model):
    class Meta:
        verbose_name = "Работа"

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="works",
    )
    who = models.CharField(max_length=255)
    where = models.CharField(max_length=255)
    when = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)


class Education(models.Model):
    class Meta:
        verbose_name = "Обуч"

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="edus",
    )
    who = models.CharField(max_length=255)
    where = models.CharField(max_length=255)
    when = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
