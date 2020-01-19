from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required
 

from miniGithub.models import Project, Problem

@login_required
def projects_view(request):
    current_user = request.user
    projects = Project.objects.filter(owner=current_user.id)
    return render(request, 'miniGithub/projects.html', {'projects': projects})

@login_required
def project_view(request, project_id):
    project = Project.objects.get(pk=project_id)
    project_problems = Problem.objects.filter(project=project_id)
    return render(request, 'miniGithub/project_details.html', {'project': project, 'problems': project_problems})

@login_required
def problem_view(request, project_id, problem_id):
  problem = Problem.objects.get(pk=problem_id)
  return render(request, 'miniGithub/problem_details.html', {'problem': problem})