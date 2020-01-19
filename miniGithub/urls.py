from django.contrib import admin
from django.urls import path
from miniGithub.views.auth import *
from miniGithub.views.projects import *

urlpatterns = [
    path('', projects_view, name="projects"),
    path('projects/<int:project_id>/', project_view, name='project_details'),
    path('projects/<int:project_id>/problems/<int:problem_id>/', problem_view, name='problem_details'),
    path('projects/<int:project_id>/problems/', add_problem_view, name='add_problem'),
    path('login/', login_view, name="login"),
    path('signup/', signup_view, name="signup"),
    path('logout/', user_logout, name='logout'),
]