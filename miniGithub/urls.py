from django.urls import path

from . import views
from miniGithub import stefanView

# app_name = 'miniGithub'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('project/<int:project_id>/', stefanView.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('', views.home_view, name="home"),
    path('signup/', views.signup_view, name="signup")
]