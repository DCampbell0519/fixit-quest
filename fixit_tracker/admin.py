from django.contrib import admin
from .models import Profile, Home, Vehicle, Category

# Register your models here.
admin.site.register(Profile)
admin.site.register(Home)
admin.site.register(Vehicle)
admin.site.register(Category)