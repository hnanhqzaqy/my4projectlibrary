from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import BaseModel




class CustomUser(AbstractUser, BaseModel):
    email = models.EmailField(
    unique=True,
    verbose_name="ایمیل",
    )
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ["username"]
    def __str__(self):
        return self.username