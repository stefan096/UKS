from django.contrib import admin
from django.urls import path
from miniGithub.views.auth import *
from miniGithub.views.projects import *

urlpatterns = [
    path('', projects_view, name="projects"),
    path('projects/<int:project_id>/', project_view, name='project_details'),
    path('projects/add_edit/<int:project_id>/', project_add_edit, name='project_add_edit'),
    path('projects/add_edit/<int:project_id>/project_save', project_save, name='project_save'),
    path('projects/<int:project_id>/problems/<int:problem_id>/', problem_view, name='problem_details'),
    path('login/', login_view, name="login"),
    path('signup/', signup_view, name="signup"),
    path('logout/', user_logout, name='logout'),
]