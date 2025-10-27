import random

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

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

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_description = models.TextField(max_length=350, blank=True, null=True)
    home = models.ForeignKey(Home, null=True, blank=True, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Categories'

    def clean(self):
        if not self.home and not self.vehicle:
            raise ValidationError('A Category must be linked to either a Home or a Vehicle')
        if self.home and self.vehicle:
            raise ValidationError('A Category can not be linked to both a Home and a Vehicle')

    def __str__(self):
        return f'{self.category_name}'

class Task(models.Model):
    task_name = models.CharField(max_length=100)
    task_description = models.TextField(max_length=350, blank=True, null=True)
    task_xp_reward = models.IntegerField(default=10)
    task_xp_random = models.IntegerField(default=0, blank=True, null=True)
    task_is_complete = models.BooleanField(default=False)
    task_date_created = models.DateField('Date Created', auto_now_add=True)
    task_date_completed = models.DateField('Date Completed', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.task_name} created on {self.task_date_created}'

    def xp_randomizer(self):
        task_xp_random = random.randint(0, 5)
        task_xp_reward = task_xp_reward + task_xp_random

    def clean(self):
        if not self.category:
            raise ValidationError('A Task must be linked to a Category')

    def save(self, *args, **kwargs):
        if self.task_is_complete and not self.task_date_completed:
            self.task_date_completed = timezone.now().date()

            if self.task_xp_random == 0:
                self.task_xp_random = random.randint(0, 5)
            
            total_xp = self.task_xp_reward + self.task_xp_random

            profile = None
            if self.category.home:
                profile = self.category.home.profile
            elif self.category.vehicle:
                profile = self.category.vehicle.profile
            
            if profile:
                profile.xp += total_xp
                profile.save()
        super().save(*args, **kwargs)