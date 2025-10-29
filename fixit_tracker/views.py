from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Profile, Home, Vehicle, Category, Task

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

class CategoryCreate(CreateView):
    model = Category
    fields = '__all__'
    success_url = '/profile/'

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)

class CategoryList(ListView):
    model = Category
    template_name = 'profile/category_list.html'
    context_object_name = 'categories'
    # def get_queryset(self):
    #     return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_categories'] = Category.objects.filter(home__isnull=False, vehicle__isnull=True)
        context['vehicle_categories'] = Category.objects.filter(vehicle__isnull=False, home__isnull=True)
        return context

class CategoryUpdate(UpdateView):
    model = Category
    fields = '__all__'
    success_url = '/category/list/'

class CategoryDelete(DeleteView):
    model = Category
    success_url = '/category/list/'

class TaskCreate(CreateView):
    model = Task
    fields = ['task_name', 'task_description', 'task_notes', 'task_image', 'category']
    success_url = '/profile/'

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)

class TaskList(ListView):
    model = Task
    template_name = 'profile/task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_tasks'] = Task.objects.filter(category__home__isnull=False, category__vehicle__isnull=True, task_is_complete=False)
        context['vehicle_tasks'] = Task.objects.filter(category__vehicle__isnull=False, category__home__isnull=True, task_is_complete=False)
        context['completed_home_tasks'] = Task.objects.filter(category__home__isnull=False, category__vehicle__isnull=True, task_is_complete=True)
        context['completed_vehicle_tasks'] = Task.objects.filter(category__vehicle__isnull=False, category__home__isnull=True, task_is_complete=True)
        return context
    
        

class TaskDetail(DetailView):
    model = Task
    template_name = 'profile/task_detail.html'
    
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        if 'complete' in request.POST:
            task.task_is_complete = True
            task.save()
        
        return redirect(reverse('task-detail', kwargs={'pk': task.pk }))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object
        if task.category.home:
            context['home_photo'] = task.category.home.home_photo
        if task.category.vehicle:
            context['vehicle_photo'] = task.category.vehicle.vehicle_photo
        return context 

class TaskUpdate(UpdateView):
    model = Task
    fields = ['task_name', 'task_description', 'task_notes', 'task_image', 'category']
    
    def get_success_url(self):
        return reverse('task-detail', kwargs={'pk': self.object.pk})

class TaskDelete(DeleteView):
    model = Task
    success_url = '/task/list/'