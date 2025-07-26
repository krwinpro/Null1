# myapp/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/<slug:category_slug>/', views.post_list, name='post_list'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<slug:category_slug>/create/', views.post_create, name='post_create'),
    path('create/', views.post_create_general, name='post_create_general'),
    path('announcement/create/', views.announcement_create, name='announcement_create'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]
