from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q

# Create your views here.

from django.contrib.auth.decorators import login_required

from miniGithub.forms import ProblemForm
from miniGithub.models import Project, Problem, Profile, Comment
from django.contrib import messages


@login_required
def projects_view(request):
    current_user = request.user
    projects = Project.objects.filter(owner=current_user.id)
    collaborations = Project.objects.filter(collaborators=current_user.id)
    return render(request, 'miniGithub/projects.html', {'projects': projects})


@login_required
def project_view(request, project_id, tab_name):
    project = get_object_or_404(Project, pk=project_id)
    project_problems = []
    if (tab_name == 'problems'):
        project_problems = Problem.objects.filter(project=project_id)
    return render(request, 'miniGithub/project_details.html',
                  {'project': project, 'problems': project_problems, 'tab_name': tab_name})


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
    problem = get_object_or_404(Problem, pk=problem_id)
    comments = Comment.objects.filter(problem=problem.id)
    reported_by = comments.first()
    return render(request, 'miniGithub/problem_details.html', {'problem': problem, 'comments': comments, 'reported_by': reported_by})


@login_required
def add_problem_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProblemForm(request.POST)
    if form.is_valid():
        current_user = request.user
        title = form.cleaned_data.get('title')
        description = form.cleaned_data.get('description')
        problem = Problem.create(title, description, project, current_user)
        return redirect(reverse('project_details', kwargs={'project_id': project_id, 'tab_name': 'problems'}))
    else:
        form = ProblemForm()
    return render(request, 'miniGithub/add_problem.html', {'form': form, 'project': project})


@login_required
def collaborators_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    collaborators = project.collaborators.all().filter(~Q(id=request.user.id)).filter(~Q(id=project.owner.id))
    return render(request, 'miniGithub/collaborators_view.html', {'collaborators': collaborators})


@login_required
def delete_collaborator(request, project_id, collaborator_id):
    project = get_object_or_404(Project, pk=project_id)
    project.collaborators.remove(collaborator_id)
    return redirect(reverse('collaborators_view', args=[project_id]))


@login_required
def add_collaborator_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'miniGithub/add_collaborator_view.html', {'project': project})


@login_required
def add_collaborator(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    email = request.POST['email']
    profile = get_object_or_404(Profile, email=email)

    collaborators = project.collaborators.all().filter(email=email)

    if project.owner.id == profile.id:
        messages.info(request, 'You are already owner of this project!')
    elif collaborators:
        messages.info(request, 'User is already collaborator on this project!')
        # that means query set is not empty so i cant add user that is already collaborator
    else:
        temp_collaborators = list(project.collaborators.all())
        temp_collaborators.append(profile.user)
        project.collaborators.set(temp_collaborators)
        project.save()
        messages.info(request, 'Successfully added collaborator')

    return redirect(reverse('add_collaborator_view', args=[project_id]))
