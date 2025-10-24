from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Home(models.Model):
    home_address = models.CharField(max_length=100)
    home_sqft = models.IntegerField()
    home_bedrooms = models.IntegerField()
    home_bathrooms = models.IntegerField()
    home_acquired = models.DateField()
    home_photo = models.ImageField(upload_to='home_photos/', blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.home_address} ({self.profile.user.username})'

class Vehicle(models.Model):
    vehicle_make = models.CharField(max_length=30)
    vehicle_model = models.CharField(max_length=30)
    vehicle_year = models.IntegerField()
    vehicle_name = models.CharField(max_length=50, blank=True)
    vehicle_photo = models.ImageField(upload_to='vehicle_photos/', blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.vehicle_year} {self.vehicle_make} {self.vehicle_model} ({self.profile.user.username})' 

