from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Profile, Home, Vehicle

# Create your views here.
class HomeView(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

def profile(request):
    profile = Profile.objects.get(user=request.user)
    homes = Home.objects.filter(profile=profile)
    vehicles = Vehicle.objects.filter(profile=profile)
    return render(request, 'profile/profile.html', {'profile': profile, 'homes': homes, 'vehicles': vehicles })

class HomeCreate(CreateView):
    model = Home
    fields = ['home_address', 'home_sqft', 'home_bedrooms', 'home_bathrooms', 'home_acquired', 'home_photo']
    success_url = '/profile/'

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)

class HomeUpdate(UpdateView):
    model = Home
    fields = ['home_address', 'home_sqft', 'home_bedrooms', 'home_bathrooms', 'home_acquired', 'home_photo']
    success_url = '/profile/'

class HomeDelete(DeleteView):
    model = Home
    success_url = '/profile/'

class VehicleCreate(CreateView):
    model = Vehicle
    fields = ['vehicle_name', 'vehicle_make', 'vehicle_model', 'vehicle_year', 'vehicle_photo']
    success_url = '/profile/'

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)

class VehicleUpdate(UpdateView):
    model = Vehicle
    fields = ['vehicle_name', 'vehicle_make', 'vehicle_model', 'vehicle_year', 'vehicle_photo']
    success_url = '/profile/'

class VehicleDelete(DeleteView):
    model = Vehicle
    success_url = '/profile/'