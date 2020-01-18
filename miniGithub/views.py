from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
 
from .forms import SignUpForm
from .models import Project
from django.urls import reverse

def home_view(request):
    return render(request, 'miniGithub/home.html')

def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect(reverse(''))
    else:
        form = SignUpForm()
    return render(request, 'miniGithub/signup.html', {'form': form})

# @login_required
def projects_view(request):
    projects = Project.objects.all()
    return render(request, 'miniGithub/projects.html', {'projects': projects})

def project_view(request, project_id):
    project = Project.objects.get(pk=project_id)
    return render(request, 'miniGithub/project_details.html', {'project': project})