import random
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    XP_PER_LEVEL = 100

    def level_up(self):
        expected_level = (self.xp // self.XP_PER_LEVEL) + 1
        if expected_level > self.level:
            self.level = expected_level
            self.save()
            return True
        return False
            
    @property
    def xp_to_next_level(self):
        next_threshold = self.level * self.XP_PER_LEVEL
        return next_threshold - self.xp

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
        if self.home:
            return f'{self.category_name} (Home)'
        elif self.vehicle:
            return f'{self.category_name} (Vehicle)'
        else:
            return f'{self.category_name}'

class Task(models.Model):
    task_name = models.CharField(max_length=100)
    task_description = models.TextField(max_length=350, blank=True, null=True)
    task_xp_reward = models.IntegerField(default=10)
    task_xp_random = models.IntegerField(default=0, blank=True, null=True)
    task_is_complete = models.BooleanField(verbose_name='Is Task complete?', default=False, help_text='Check the box once you have completed this task')
    task_date_created = models.DateField('Date Created', auto_now_add=True)
    task_date_completed = models.DateField('Date Completed', blank=True, null=True)
    task_notes = models.TextField(max_length=500, blank=True, null=True)
    task_image = models.ImageField(upload_to='task_photos/', blank=True, null=True, help_text='Upload photos of receipts, completed work, or reference images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.task_name} created on {self.task_date_created}'

    class Meta: 
        ordering = ['category', '-task_date_created']

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
                leveled = profile.level_up()
                profile.save()
                XPLog.objects.create(profile=profile, task=self, xp_gained=total_xp)
        super().save(*args, **kwargs)

class XPLog(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    xp_gained = models.IntegerField()
    date_logged = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile.user.username} gained {self.xp_gained} XP on {self.date_logged} for completing {self.task}'
