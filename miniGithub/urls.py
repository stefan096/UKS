from django.contrib import admin
from django.urls import path

from miniGithub.views.auth import *
from miniGithub.views.projects import *
from miniGithub.views.webhooks import *


urlpatterns = [
    path('', projects_view, name="projects"),
    path('projects/<int:project_id>/<str:tab_name>/', project_view, name='project_details'), 
    path('projects/<int:project_id>/<str:tab_name>/<str:action>', project_view_filter, name='project_view_filter'),
    path('projects/add_edit/<int:project_id>/', project_add_edit, name='project_add_edit'),
    path('projects/add_edit/<int:project_id>/project_save', project_save, name='project_save'),
    path('projects/<int:project_id>/problems/<int:problem_id>/', problem_view, name='problem_details'),
    path('projects/<int:project_id>/problems/<int:problem_id>/close/', close_problem, name='close_problem'),
    path('projects/<int:project_id>/problems/<int:problem_id>/reopen/', reopen_problem, name='reopen_problem'),
    path('projects/<int:project_id>/milestones/<int:milestone_id>/close/', close_milestone, name='close_milestone'),
    path('projects/<int:project_id>/milestones/<int:milestone_id>/open/', open_milestone, name='open_milestone'),
    path('projects/<int:project_id>/problems/<int:problem_id>/set_milestone/', set_milestone_view, name='set_milestone_view'),
    path('projects/<int:project_id>/problems/<int:problem_id>/link_labels/', link_labels_view, name='link_labels_view'),
    path('projects/<int:project_id>/problems/<int:problem_id>/link_labels/<int:label_id>/link/', link_label, name='link_label'),
    path('projects/<int:project_id>/problems/<int:problem_id>/link_labels/<int:label_id>/unlink/', unlink_label, name='unlink_label'),
    path('projects/<int:project_id>/problems/<int:problem_id>/set_milestone/<int:milestone_id>/', set_milestone, name='set_milestone'),
    path('projects/<int:project_id>/problems/<int:problem_id>/set_assignee/', set_assignee_view, name='set_assignee_view'),
    path('projects/<int:project_id>/problems/<int:problem_id>/set_assignee/save/', set_assignee, name='set_assignee'),
    path('projects/<int:project_id>/problems/<int:problem_id>/comments/<int:comment_id>/edit/', edit_comment_view, name='edit_comment'),
    path('projects/<int:project_id>/problems/<int:problem_id>/add_comment/', add_comment, name='add_comment'),
    path('projects/<int:project_id>/problems/add_problem/', add_problem_view, name='add_problem'),
    path('projects/<int:project_id>/problems/add_milestone/', add_milestone_view, name='add_milestone'),
    path('projects/<int:project_id>/problems/add_label/', add_label_view, name='add_label'),
    path('projects/<int:project_id>/labels/<int:label_id>/show/edit/', edit_label_view, name='edit_label'),
    path('projects/<int:project_id>/labels/<int:label_id>/show/', label_details, name='label_details'),
    path('projects/<int:project_id>/labels/<int:label_id>/show/<str:action>', label_details_action, name='label_details_action'),
    path('projects/<int:project_id>/problems/<int:milestone_id>/show/edit/', edit_milestone_view, name='edit_milestone'),
    path('projects/<int:project_id>/problems/<int:milestone_id>/show/', milestone_details, name='milestone_details'),
    path('projects/<int:project_id>/problems/<int:milestone_id>/show/<str:action>', milestone_details_action,
         name='milestone_details_action'),
    path('projects/<int:project_id>/collaborators', collaborators_view, name='collaborators_view'),
    path('projects/<int:project_id>/collaborators/<int:collaborator_id>/delete/', delete_collaborator, name='delete_collaborator'),
    path('collaborations/', show_collaborator_projects, name='show_collaborator_projects'),
    path('add_collaborator/<int:project_id>/view/', add_collaborator_view, name='add_collaborator_view'),
    path('add_collaborator/<int:project_id>/view/save_collaborator/', add_collaborator, name='add_collaborator'),

    path('login/', login_view, name="login"),
    path('signup/', signup_view, name="signup"),
    path('logout/', user_logout, name='logout'),
    path('api/webhook_push/', webhook_push, name='webhook_push'),
]