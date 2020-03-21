from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from datetime import datetime

# Create your views here.

from django.contrib.auth.decorators import login_required
from itertools import chain
from operator import attrgetter
from django.contrib.auth.models import User
from miniGithub.forms import ProblemForm, MilestoneForm, EditCommentForm, LabelForm
from miniGithub.models import Custom_Event, Project, Problem, Profile, Comment, Milestone, Change_Comment, Change_State, Problem_State, Change_Milestone, Change_Assignee, Change_Code, Change_Label, Label, Milestone_State
from django.contrib import messages


@login_required
def projects_view(request):
    current_user = request.user
    projects = Project.objects.filter(owner=current_user.id)
    collaborations = Project.objects.filter(collaborators=current_user.id)
    return render(request, 'miniGithub/projects.html', {'projects': projects})


@login_required
def project_view(request, project_id, tab_name):
    current_user = request.user
    project = get_object_or_404(Project, pk=project_id)
    project.is_owner = current_user == project.owner
    project_problems = []
    if tab_name == 'problems':
        project_problems = Problem.objects.filter(project=project_id)

        ret_val = []

        for one_problem in project_problems:
            state_changes = Change_State.objects.filter(problem=one_problem.id)

            if state_changes.last():
                last_change = state_changes.last()
                if state_changes.last().current_state == None:
                    one_problem.is_open = False
                elif int(state_changes.last().current_state) == Problem_State.CLOSED.value:
                    one_problem.is_open = False
                else:
                    one_problem.is_open = True
                
                if one_problem.is_open is False:
                    one_problem.closed_time = last_change.created_time
                    one_problem.closed_by = last_change.creator
            else:
                one_problem.is_open = True

            ret_val.append(one_problem)

        return render(request, 'miniGithub/project_details.html',
                      {'project': project, 'problems': ret_val, 'tab_name': tab_name})

    elif tab_name == 'collaborators':

        collaborators = project.collaborators.all().filter(~Q(id=request.user.id)).filter(~Q(id=project.owner.id))
        return render(request, 'miniGithub/project_details.html', {'project': project, 'collaborators': collaborators, 'tab_name': tab_name})

    elif tab_name == 'milestones':
        project_milestones = Milestone.objects.filter(project=project_id)
        ret_val = []

        for one_milestones in project_milestones:
            state_changes = Change_Milestone.objects.filter(current_milestone=one_milestones.id)

            if state_changes.last():
                last_change = state_changes.last()
                if state_changes.last().current_state == None:
                    one_milestones.is_open = False
                elif int(state_changes.last().current_state) == Problem_State.CLOSED.value:
                    one_milestones.is_open = False
                else:
                    one_milestones.is_open = True
                
                if one_milestones.is_open is False:
                    one_milestones.closed_time = last_change.created_time
                    one_milestones.closed_by = last_change.creator
            else:
                one_milestones.is_open = True

            ret_val.append(one_milestones)

        return render(request, 'miniGithub/project_details.html',
                  {'project': project, 'milestones': ret_val, 'tab_name': tab_name})
    elif tab_name == 'labels':
        project_labels = Label.objects.filter(project=project_id)
        return render(request, 'miniGithub/project_details.html',
                  {'project': project, 'labels': project_labels, 'tab_name': tab_name})

    return render(request, 'miniGithub/project_details.html',
                  {'project': project, 'problems': project_problems, 'tab_name': tab_name})


@login_required
def project_view_filter(request, project_id, tab_name, action):
    
    current_user = request.user
    project = get_object_or_404(Project, pk=project_id)
    project.is_owner = current_user == project.owner
    project_problems = []
    if tab_name == 'problems':
        project_problems = Problem.objects.filter(project=project_id)

        ret_val = []

        for one_problem in project_problems:
            state_changes = Change_State.objects.filter(problem=one_problem.id)
            if state_changes.last():
                last_change = state_changes.last()
                if state_changes.last().current_state == None:
                    one_problem.is_open = False
                elif int(state_changes.last().current_state) == Problem_State.CLOSED.value:
                    one_problem.is_open = False
                else:
                    one_problem.is_open = True
    
                if one_problem.is_open is False:
                    one_problem.closed_time = last_change.created_time
                    one_problem.closed_by = last_change.creator
                if one_problem.is_open is True and action == 'open':
                    ret_val.append(one_problem)
                elif one_problem.is_open is False and action == 'closed':
                    ret_val.append(one_problem)
                elif action == -1:
                    ret_val.append(one_problem)
            else:
                one_problem.is_open = True

                if one_problem.is_open is True and action == 'open':
                    ret_val.append(one_problem)
                elif one_problem.is_open is False and action == 'closed':
                    ret_val.append(one_problem)
                elif action == -1:
                    ret_val.append(one_problem)

        return render(request, 'miniGithub/project_details.html',
                      {'project': project, 'problems': ret_val, 'tab_name': tab_name, 'filter': action})
    elif tab_name == 'milestones':
        project_milestones = Milestone.objects.filter(project=project_id)
        ret_val = []

        for one_milestones in project_milestones:
            state_changes = Change_Milestone.objects.filter(current_milestone=one_milestones.id)

            if state_changes.last():
                last_change = state_changes.last()
                if state_changes.last().current_state == None:
                    one_milestones.is_open = False
                elif int(state_changes.last().current_state) == Problem_State.CLOSED.value:
                    one_milestones.is_open = False
                else:
                    one_milestones.is_open = True

                if one_milestones.is_open is False:
                    one_milestones.closed_time = last_change.created_time
                    one_milestones.closed_by = last_change.creator
                
                if one_milestones.is_open is True and action == 'open':
                    ret_val.append(one_milestones)
                elif one_milestones.is_open is False and action == 'closed':
                    ret_val.append(one_milestones)
                elif action == -1:
                    ret_val.append(one_milestones)
            else:
                one_milestones.is_open = True

                if one_milestones.is_open is True and action == 'open':
                    ret_val.append(one_milestones)
                elif one_milestones.is_open is False and action == 'closed':
                    ret_val.append(one_milestones)
                elif action == -1:
                    ret_val.append(one_milestones)

        return render(request, 'miniGithub/project_details.html',
                  {'project': project, 'milestones': ret_val, 'tab_name': tab_name, 'filter': action})

    return render(request, 'miniGithub/project_details.html',
                  {'project': project, 'problems': project_problems, 'tab_name': tab_name, 'filter': action})


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
    state_changes = Change_State.objects.filter(problem=problem.id)
    milestone_changes = Change_Milestone.objects.filter(problem=problem.id)
    assignee_changes = Change_Assignee.objects.filter(problem=problem.id)
    code_changes = Change_Code.objects.filter(problem=problem.id)
    label_changes = Change_Label.objects.filter(problem=problem.id)
    for assignment in assignee_changes:    
        print(assignment.assignee is None)
    if (state_changes.last()):
        problem.is_open = int(state_changes.last().current_state) != Problem_State.CLOSED.value
    else:
        problem.is_open = True
    for comment in comments:
        edits = Change_Comment.objects.filter(relatedComment=comment.id)
        comment.editCounts = edits.count()
        comment.edits = edits
        comment.editsSorted = edits[::-1]
    timeline = sorted(chain(comments, state_changes, milestone_changes, assignee_changes, code_changes, label_changes), key=attrgetter('created_time'))
    labels = problem.labels.all()
    return render(request, 'miniGithub/problem_details.html', {'problem': problem, 'timeline': timeline, 'labels': labels})


@login_required
def set_milestone_view(request, project_id, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    project_milestones = Milestone.objects.filter(project=project_id)
    return render(request, 'miniGithub/link_milestone.html', {'problem': problem, 'milestones': project_milestones})


@login_required
def link_labels_view(request, project_id, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    labels = Label.objects.filter(project=project_id)
    for label in labels:
        if problem.labels.filter(id=label.id).exists():
            label.linked = True
        else:
            label.linked = False
    return render(request, 'miniGithub/link_labels.html', {'problem': problem, 'labels': labels})

@login_required
def unlink_label(request, project_id, problem_id, label_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    label = get_object_or_404(Label, pk=label_id)
    current_user = request.user
    problem = problem.remove_label(current_user, label)
    return redirect(reverse('problem_details', args=[project_id, problem_id]))

@login_required
def link_label(request, project_id, problem_id, label_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    label = get_object_or_404(Label, pk=label_id)
    current_user = request.user
    problem = problem.add_label(current_user, label)
    return redirect(reverse('problem_details', args=[project_id, problem_id]))
    
@login_required
def set_milestone(request, project_id, problem_id, milestone_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    current_user = request.user
    problem = problem.link_to_milestone(current_user, milestone)
    return redirect(reverse('problem_details', args=[project_id, problem_id]))


@login_required
def close_milestone(request, project_id, milestone_id):
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    current_user = request.user
    milestone.close_milestone(current_user)
    return redirect(reverse('milestone_details', kwargs={'project_id': project_id, 'milestone_id': milestone_id}))


@login_required
def open_milestone(request, project_id, milestone_id):
    milestone = get_object_or_404(Milestone, pk=milestone_id)
    current_user = request.user
    milestone.open_milestone(current_user)
    return redirect(reverse('milestone_details', kwargs={'project_id': project_id, 'milestone_id': milestone_id}))

@login_required
def set_assignee_view(request, project_id, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    project = get_object_or_404(Project, pk=project_id)
    project_collaborators =  list(project.collaborators.all())
    project_collaborators.append(project.owner)
    project_collaborators = list(filter(lambda item: item != problem.current_assignee, project_collaborators))
    return render(request, 'miniGithub/assign_user.html', {'problem': problem, 'collaborators': project_collaborators})


@login_required
def set_assignee(request, project_id, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    assignee_id = request.POST['assignee']
    current_user = request.user
    if (assignee_id == ""):
        problem = problem.assign_user(current_user, None)
    else:
        user = get_object_or_404(User, pk=assignee_id)
        problem = problem.assign_user(current_user, user)
    return redirect(reverse('problem_details', args=[project_id, problem_id]))


@login_required
def edit_comment_view(request, project_id, problem_id, comment_id): 
    comment = get_object_or_404(Comment, pk=comment_id)
    form = EditCommentForm(request.POST, initial={"description": comment.description})
    if form.is_valid():
        current_user = request.user
        description = form.cleaned_data.get('description')
        comment = comment.edit(current_user, description)
        return redirect(reverse('problem_details', args=[project_id, problem_id]))
    else:
        form = EditCommentForm(initial={"description": comment.description})
    return render(request, 'miniGithub/edit_comment.html', {'form': form, 'comment': comment, "project_id": project_id, "problem_id": problem_id})


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
def add_milestone_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = MilestoneForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data.get('title')
        description = form.cleaned_data.get('description')
        due_date = form.cleaned_data.get('due_date')
        created_time = datetime.now()
        milestone = Milestone(title=title, description=description, due_date=due_date, created_time=created_time,
                              project=project)
        milestone.save()
        return redirect(reverse('project_details', kwargs={'project_id': project_id, 'tab_name': 'milestones'}))
    else:
        form = MilestoneForm()
    return render(request, 'miniGithub/add_milestone.html', {'form': form, 'project': project})

@login_required
def add_label_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = LabelForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data.get('title')
        color = form.cleaned_data.get('color')
        label = Label(title=title, color=color, project=project)
        label.save()
        return redirect(reverse('project_details', kwargs={'project_id': project_id, 'tab_name': 'labels'}))
    else:
        form = LabelForm()
    return render(request, 'miniGithub/add_label.html', {'form': form, 'project': project})

@login_required
def edit_label_view(request, project_id, label_id):
    project = get_object_or_404(Project, pk=project_id)
    form = LabelForm(request.POST)
    if form.is_valid():
        label = Label.objects.get(pk=label_id)
        label.title = form.cleaned_data.get('title')
        label.color = form.cleaned_data.get('color')
        label.save()
        return redirect(reverse('project_details', kwargs={'project_id': project_id, 'tab_name': 'labels'}))
    else:
        found_label = Label.objects.get(pk=label_id)
    return render(request, 'miniGithub/edit_label.html', {'form': form, 'project': project, 'label': found_label})


@login_required
def label_details(request, project_id, label_id):
    project = get_object_or_404(Project, pk=project_id)
    label = Label.objects.get(pk=label_id)
    problems = Problem.objects.filter(labels=label.id)

    for one_problem in problems:
        state_changes = Change_State.objects.filter(problem=one_problem.id)
        if state_changes.last():
            last_change = state_changes.last()
            one_problem.is_open = one_problem.is_open = int(state_changes.last().current_state) != Problem_State.CLOSED.value
        
            if one_problem.is_open is False:
                one_problem.closed_time = last_change.created_time
                one_problem.closed_by = last_change.creator

        else:
            one_problem.is_open = True

    return render(request, 'miniGithub/label_details.html', {'project': project, 'label': label,
                                                                 'problems': problems})


@login_required
def label_details_action(request, project_id, label_id, action):
    project = get_object_or_404(Project, pk=project_id)
    label = Label.objects.get(pk=label_id)
    problems = Problem.objects.filter(labels=label.id)
    ret_val = []

    for one_problem in problems:
        state_changes = Change_State.objects.filter(problem=one_problem.id)
        if state_changes.last():
            last_change = state_changes.last()
            one_problem.is_open = one_problem.is_open = int(state_changes.last().current_state) != Problem_State.CLOSED.value

            if one_problem.is_open is False:
                one_problem.closed_time = last_change.created_time
                one_problem.closed_by = last_change.creator

            if one_problem.is_open is True and action == 'open':
                ret_val.append(one_problem)
            elif one_problem.is_open is False and action == 'closed':
                ret_val.append(one_problem)
        else:
            one_problem.is_open = True

            if one_problem.is_open is True and action == 'open':
                ret_val.append(one_problem)
            elif one_problem.is_open is False and action == 'closed':
                ret_val.append(one_problem)

    return render(request, 'miniGithub/label_details.html', {'project': project, 'label': label,
                                                                 'problems': ret_val, 'filter': action})


@login_required
def edit_milestone_view(request, project_id, milestone_id):
    project = get_object_or_404(Project, pk=project_id)
    form = MilestoneForm(request.POST)
    if form.is_valid():
        milestone = Milestone.objects.get(pk=milestone_id)
        milestone.title = form.cleaned_data.get('title')
        milestone.description = form.cleaned_data.get('description')
        milestone.due_date = form.cleaned_data.get('due_date')
        #milestone.created_time = datetime.now()
        #treba videti kad se edituje da li treba da se generise novi dogadjaj
        milestone.save()
        return redirect(reverse('project_details', kwargs={'project_id': project_id, 'tab_name': 'milestones'}))
    else:
        found_milestone = Milestone.objects.get(pk=milestone_id)
        found_milestone.due_date = str(found_milestone.due_date.date())
    return render(request, 'miniGithub/edit_milestone.html', {'form': form, 'project': project, 'milestone': found_milestone})


@login_required
def milestone_details(request, project_id, milestone_id):
    project = get_object_or_404(Project, pk=project_id)
    found_milestone = Milestone.objects.get(pk=milestone_id)
    problems = Problem.objects.filter(linked_milestone=found_milestone)
    state_changes = Change_Milestone.objects.filter(current_milestone=milestone_id)
    if state_changes.last():
        last_change = state_changes.last()
        if state_changes.last().current_state == None:
            found_milestone.is_open = False
        elif int(state_changes.last().current_state) == Milestone_State.CLOSED.value:
            found_milestone.is_open = False
        else:
            found_milestone.is_open = True

        if found_milestone.is_open is False:
            found_milestone.closed_time = last_change.created_time
            found_milestone.closed_by = last_change.creator
    else:
        found_milestone.is_open = True

    for one_problem in problems:
        state_changes = Change_State.objects.filter(problem=one_problem.id)
        if state_changes.last():
            last_change = state_changes.last()
            one_problem.is_open = one_problem.is_open = int(state_changes.last().current_state) != Problem_State.CLOSED.value
            
            if one_problem.is_open is False:
                one_problem.closed_time = last_change.created_time
                one_problem.closed_by = last_change.creator
        else:
            one_problem.is_open = True

    return render(request, 'miniGithub/milestone_details.html', {'project': project, 'milestone': found_milestone,
                                                                 'problems': problems})


@login_required
def milestone_details_action(request, project_id, milestone_id, action):
    project = get_object_or_404(Project, pk=project_id)
    found_milestone = Milestone.objects.get(pk=milestone_id)
    problems = Problem.objects.filter(linked_milestone=found_milestone)
    ret_val = []
    state_changes = Change_Milestone.objects.filter(current_milestone=milestone_id)
    if state_changes.last():
        last_change = state_changes.last()
        if state_changes.last().current_state == None:
            found_milestone.is_open = False
        elif int(state_changes.last().current_state) == Milestone_State.CLOSED.value:
            found_milestone.is_open = False
        else:
            found_milestone.is_open = True

        if found_milestone.is_open is False:
            found_milestone.closed_time = last_change.created_time
            found_milestone.closed_by = last_change.creator
    else:
        found_milestone.is_open = True

    for one_problem in problems:
        state_changes = Change_State.objects.filter(problem=one_problem.id)
        if state_changes.last():
            last_change = state_changes.last()
            one_problem.is_open = one_problem.is_open = int(last_change.current_state) != Problem_State.CLOSED.value

            if one_problem.is_open is False:
                one_problem.closed_time = last_change.created_time
                one_problem.closed_by = last_change.creator

            if one_problem.is_open is True and action == 'open':
                ret_val.append(one_problem)
            elif one_problem.is_open is False and action == 'closed':
                ret_val.append(one_problem)
        else:
            one_problem.is_open = True

            if one_problem.is_open is True and action == 'open':
                ret_val.append(one_problem)
            elif one_problem.is_open is False and action == 'closed':
                ret_val.append(one_problem)

    return render(request, 'miniGithub/milestone_details.html', {'project': project, 'milestone': found_milestone,
                                                                 'problems': ret_val, 'filter': action})


@login_required
def add_comment(request, project_id, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    comment = request.POST['comment']
    current_user = request.user
    created_comment = Comment.create(current_user, comment, problem)
    return redirect(reverse('problem_details', args=[project_id, problem_id]))


@login_required
def close_problem(request, project_id, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    current_user = request.user
    problem.close_problem(current_user)
    return redirect(reverse('problem_details', args=[project_id, problem_id]))


def reopen_problem(request, project_id, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    current_user = request.user
    problem.reopen_problem(current_user)
    return redirect(reverse('problem_details', args=[project_id, problem_id]))


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


@login_required
def show_collaborator_projects(request):
    current_user = request.user
    projects = Project.objects.filter(collaborators=current_user)

    return render(request, 'miniGithub/show_collaborator_projects.html', {'projects': projects})