from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import HomeForm
from .models import Profile, Home, Vehicle, Category, Task, XPLog

# Create your views here.
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            profile = Profile()
            profile.user = user
            profile.save()
            return redirect('profile')
        else:
            error_message = 'Invalid sign up - Please try again.'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

class HomeView(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    homes = Home.objects.filter(profile=profile)
    vehicles = Vehicle.objects.filter(profile=profile)
    completed_home_tasks = Task.objects.filter(category__home__profile=profile, task_is_complete=True).count()
    pending_home_tasks = Task.objects.filter(category__home__profile=profile, task_is_complete=False).count()
    completed_vehicle_tasks = Task.objects.filter(category__vehicle__profile=profile, task_is_complete=True).count()
    pending_vehicle_tasks = Task.objects.filter(category__vehicle__profile=profile, task_is_complete=False).count()
    xp_logs = XPLog.objects.filter(profile=profile).order_by('-date_logged')[:5]
    return render(request, 'profile/profile.html', {'profile': profile, 'homes': homes, 'vehicles': vehicles, 'completed_home_tasks': completed_home_tasks, 'pending_home_tasks': pending_home_tasks, 'pending_vehicle_tasks': pending_vehicle_tasks, 'completed_vehicle_tasks': pending_vehicle_tasks, 'xp_logs': xp_logs })

class HomeCreate(LoginRequiredMixin, CreateView):
    model = Home
    success_url = '/profile/'
    form_class = HomeForm

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)

class HomeUpdate(LoginRequiredMixin, UpdateView):
    model = Home
    fields = ['home_address', 'home_sqft', 'home_bedrooms', 'home_bathrooms', 'home_acquired', 'home_photo']
    success_url = '/profile/'

class HomeDelete(LoginRequiredMixin, DeleteView):
    model = Home
    success_url = '/profile/'

class VehicleCreate(LoginRequiredMixin, CreateView):
    model = Vehicle
    fields = ['vehicle_name', 'vehicle_make', 'vehicle_model', 'vehicle_year', 'vehicle_photo']
    success_url = '/profile/'

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)

class VehicleUpdate(LoginRequiredMixin, UpdateView):
    model = Vehicle
    fields = ['vehicle_name', 'vehicle_make', 'vehicle_model', 'vehicle_year', 'vehicle_photo']
    success_url = '/profile/'

class VehicleDelete(LoginRequiredMixin, DeleteView):
    model = Vehicle
    success_url = '/profile/'

class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = '__all__'
    success_url = '/category/list/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user_profile = self.request.user.profile
        form.fields['home'].queryset = Home.objects.filter(profile=user_profile)
        form.fields['vehicle'].queryset = Vehicle.objects.filter(profile=user_profile)
        return form

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)

class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'profile/category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.profile
        context['home_categories'] = Category.objects.filter(home__profile=user_profile, vehicle__isnull=True)
        context['vehicle_categories'] = Category.objects.filter(vehicle__profile=user_profile, home__isnull=True)
        return context

class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    fields = '__all__'
    success_url = '/category/list/'

class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = '/category/list/'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['task_name', 'task_description', 'task_notes', 'task_image', 'category']
    success_url = '/task/list/'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user_profile = self.request.user.profile
        form.fields['category'].queryset = Category.objects.filter(Q(home__profile=user_profile) | Q(vehicle__profile=user_profile)).order_by('home', 'vehicle', 'category_name') 
        return form

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'profile/task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.profile
        context['home_tasks'] = Task.objects.filter(category__home__profile=user_profile, category__vehicle__isnull=True, task_is_complete=False)
        context['vehicle_tasks'] = Task.objects.filter(category__vehicle__profile=user_profile, category__home__isnull=True, task_is_complete=False)
        context['completed_home_tasks'] = Task.objects.filter(category__home__profile=user_profile, category__vehicle__isnull=True, task_is_complete=True)
        context['completed_vehicle_tasks'] = Task.objects.filter(category__vehicle__profile=user_profile, category__home__isnull=True, task_is_complete=True)
        return context
    
class TaskDetail(LoginRequiredMixin, DetailView):
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

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['task_name', 'task_description', 'task_notes', 'task_image', 'category']
    
    def get_success_url(self):
        return reverse('task-detail', kwargs={'pk': self.object.pk})

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = '/task/list/'