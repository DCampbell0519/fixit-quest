from django.urls import path
from . import views



urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('home/create/', views.HomeCreate.as_view(), name='home-create'),
    path('home/<int:pk>/update/', views.HomeUpdate.as_view(), name='home-update'),
    path('home/<int:pk>/delete/', views.HomeDelete.as_view(), name='home-delete'),
    path('vehicle/create/', views.VehicleCreate.as_view(), name='vehicle-create'),
    path('vehicle/<int:pk>/update/', views.VehicleUpdate.as_view(), name='vehicle-update'),
    path('vehicle/<int:pk>/delete/', views.VehicleDelete.as_view(), name='vehicle-delete'),

]