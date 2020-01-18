from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name="signup"),
    path('projects/', views.projects_view, name="projects"),
    path('projects/<int:project_id>/', views.project_view, name='project_details'),
    path('', views.home_view, name="home")
]