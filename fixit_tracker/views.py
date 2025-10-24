from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.views import LoginView

# Create your views here.
class Home(LoginView):
    template_name = 'home.html'

# def home(request):
#     return HttpResponse('<h1>Welcome to FixIt Quest!</h1>')

def about(request):
    return render(request, 'about.html')