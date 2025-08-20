from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.create_post, name='create_post'),
    path('<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('<slug:slug>/like/', views.like_post, name='like_post'),
    path('<slug:slug>/dislike/', views.dislike_post, name='dislike_post'),
    path('<slug:slug>/delete/', views.delete_post, name='delete_post'),
    path('user/<str:username>/', views.user_posts, name='user_posts'),
]
