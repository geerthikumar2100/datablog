from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.list_posts, name='home'),  # Dashboard as home page
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_post, name='create_post'),
    path('posts/', views.all_posts, name='list_posts'),
    path('edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

