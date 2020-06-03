from django.db import models
from django.contrib.auth.models import User
from .models import *
from import_export.admin import ImportExportModelAdmin

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #1대1 조인
    OwnerName = models.TextField(max_length=10)
    OwnerPhone = models.CharField(max_length=13)
    StoreName = models.CharField(max_length=32)
    StorePhone = models.CharField(max_length=13)
    StoreAddress = models.CharField(max_length=32)
    Latitude = models.FloatField(default=None)
    Longitude = models.FloatField(default=None)
    OwnerType = models.CharField(max_length=13, blank=True)

    def __str__(self):
        return self.StoreName