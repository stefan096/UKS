from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

# Create your views here.

from django.contrib.auth.decorators import login_required
 
from miniGithub.forms import ProblemForm
from miniGithub.models import Project, Problem

@login_required
def projects_view(request):
    current_user = request.user
    projects = Project.objects.filter(owner=current_user.id)
    return render(request, 'miniGithub/projects.html', {'projects': projects})

@login_required
def project_view(request, project_id, tab_name):
  project = get_object_or_404(Project, pk=project_id)
  project_problems = []
  if (tab_name == 'problems'):
    project_problems = Problem.objects.filter(project=project_id)
  print(project_problems)
  return render(request, 'miniGithub/project_details.html', {'project': project, 'problems': project_problems, 'tab_name': tab_name})

@login_required
def problem_view(request, project_id, problem_id):
  problem = get_object_or_404(Problem, pk=problem_id)
  
  return render(request, 'miniGithub/problem_details.html', {'problem': problem})

@login_required
def add_problem_view(request, project_id):
  project = get_object_or_404(Project, pk=project_id)
  form = ProblemForm(request.POST)
  if form.is_valid():
    current_user = request.user
    title = form.cleaned_data.get('title')
    description = form.cleaned_data.get('description')
    problem = Problem.create(title, description, project, current_user)
    return redirect(reverse('project_details', kwargs={'project_id':project_id, 'tab_name': 'problems'}))
  else:
      form = ProblemForm()
  return render(request, 'miniGithub/add_problem.html', {'form': form, 'project': project})