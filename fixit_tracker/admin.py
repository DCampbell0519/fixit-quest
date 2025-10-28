from django.contrib import admin
from .models import Profile, Home, Vehicle, Category, Task

# Register your models here.
admin.site.register(Profile)
admin.site.register(Home)
admin.site.register(Vehicle)
admin.site.register(Category)
admin.site.register(Task)