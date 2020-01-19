# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

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
def project_add_edit(request, project_id):
    if project_id:
        project = Project.objects.get(pk=project_id)
    else:
        project = Project()
    return render(request, 'miniGithub/project_add_edit.html', {'project': project})


@login_required
def project_save(request, project_id):
    if project_id:
        found_project = Project.objects.get(id=project_id)
    else:
        found_project = Project()

    found_project.title = request.POST['title']
    found_project.git_repo = request.POST['git_repo']

    current_user = request.user
    found_project.owner = current_user
    found_project.save()

    return redirect(reverse('projects'))


@login_required
def problem_view(request, project_id, problem_id):
    problem = Problem.objects.get(pk=problem_id)
    return render(request, 'miniGithub/problem_details.html', {'problem': problem})

