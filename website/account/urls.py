from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('login/',LoginView.as_view(template_name='account/login.html'),name='login'),
]
