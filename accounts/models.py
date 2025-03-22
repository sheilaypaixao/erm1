from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Permission

from companies.models import Enterprise
# Create your models here.

class Grouping(models.Model):
    name = models.CharField(max_length=85)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    #members = models.ManyToManyField(User, through="User_Grouping")
    permissions = models.ManyToManyField(Permission, through="Grouping_Permissions")

class User(AbstractBaseUser):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    is_owner = models.BooleanField(default=True)
    grouping = models.ForeignKey(Grouping, on_delete=models.PROTECT, null=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Grouping_Permissions(models.Model):
    grouping = models.ForeignKey(Grouping, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

#class User_Grouping(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #grouping = models.ForeignKey(Grouping, on_delete=models.CASCADE)