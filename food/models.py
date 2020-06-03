from django.db import models
from login.models import Profile

# Create your models here.
class Foodmenu(models.Model):
    StoreName=models.CharField(max_length=32)
    Menu=models.CharField(max_length=32)
    Price=models.IntegerField()
    Category=models.CharField(max_length=10)
    Latitude=models.FloatField(default=None)
    Longitude=models.FloatField(default=None)
    Foodurl=models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.Menu

class Store(models.Model):
    StoreName=models.CharField(max_length=32)
    StoreAddress=models.CharField(max_length=32)
    StorePhone=models.CharField(max_length=13)
    Latitude=models.FloatField(default=None)
    Longitude=models.FloatField(default=None)

    def __str__(self):
        return self.StoreName

class Dessertmenu(models.Model):
    StoreName=models.CharField(max_length=32)
    Menu=models.CharField(max_length=32)
    Price=models.IntegerField()
    Category=models.CharField(max_length=10)
    Latitude=models.FloatField(default=None)
    Longitude=models.FloatField(default=None)
    Foodurl=models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.Menu