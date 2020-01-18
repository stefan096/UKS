from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects_view, name="projects"),
    path('projects/<int:project_id>/', views.project_view, name='project_details'),
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', views.user_logout, name='logout'),
]