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
    path('category/create/', views.CategoryCreate.as_view(), name='category-create'),
    path('category/list/', views.CategoryList.as_view(), name='category-list'),
    path('category/<int:pk>/update', views.CategoryUpdate.as_view(), name='category-update'),
    path('category/<int:pk>/delete', views.CategoryDelete.as_view(), name='category-delete'),
]