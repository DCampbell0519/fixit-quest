from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from .models import Profile, Home, Vehicle

# Create your views here.
class HomeView(LoginView):
    template_name = 'home.html'

# def home(request):
#     return HttpResponse('<h1>Welcome to FixIt Quest!</h1>')

def about(request):
    return render(request, 'about.html')

def profile(request):
    profile = Profile.objects.get(user=request.user)
    homes = Home.objects.filter(profile=profile)
    vehicles = Vehicle.objects.filter(profile=profile)
    return render(request, 'profile/profile.html', {'profile': profile, 'homes': homes, 'vehicles': vehicles })