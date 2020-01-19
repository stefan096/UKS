from django.shortcuts import render

# Create your views here.

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect


from miniGithub.forms import LoginForm, SignUpForm
from django.urls import reverse
from django.contrib import messages

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
        return redirect(reverse('projects'))
    else:
        form = SignUpForm()
    return render(request, 'miniGithub/signup.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect(reverse('projects'))
        else:
            messages.info(request, 'Wrong email or password!')
            form = LoginForm()
            return render(request, 'miniGithub/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'miniGithub/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect(reverse('login'))
