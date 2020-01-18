
from django.http import HttpResponse
# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from miniGithub.models import Project
from django.http import Http404


def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")

    # latest_question_list = Project.objects.order_by('title')[:5]
    # output = ', '.join([p.title for p in latest_question_list])
    # return HttpResponse(output)

    latest_question_list = Project.objects.order_by('title')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'miniGithub/index.html', context)

# Leave the rest of the views (detail, results, vote) unchanged

def detail(request, project_id):
    #return HttpResponse("You're looking at question %s." % question_id)

    # try:
    #     project = Project.objects.get(pk=question_id)
    # except Project.DoesNotExist:
    #     raise Http404("project does not exist")
    # return render(request, 'miniGithub/detail.html', {'project': project})

    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'miniGithub/detail.html', {'project': project})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def home_view(request):
    return render(request, 'home.html')

def signup_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'miniGithub/signup.html', {'form': form})
