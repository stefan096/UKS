from enum import Enum

from django.db import models

# Create your models here.

LENGTH_OF_FIELD = 100
LENGTH_OF_FIELD_AREA = 500


class Project(models.Model):
    title = models.CharField(max_length=LENGTH_OF_FIELD)
    git_repo = models.CharField(max_length=LENGTH_OF_FIELD)


class Problem(models.Model):
    title = models.CharField(max_length=LENGTH_OF_FIELD)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    base_problem = models.ForeignKey('self', on_delete=models.CASCADE)


class User(models.Model):
    name: models.CharField(max_length=LENGTH_OF_FIELD)
    email: models.CharField(max_length=LENGTH_OF_FIELD)


class Event(models.Model):
    created_time: models.DateTimeField
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)


class Comment(Event):
    description: models.CharField(max_length=LENGTH_OF_FIELD_AREA)


class Problem_State(Enum):
    OPEN = 1
    CLOSED = 2


class Change_State(Event):
    new_state: models.CharField(
      max_length=2,
      choices=[(tag, tag.value) for tag in Problem_State]
    )


class Change_Assignee(Event):
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)


class Milestone(models.Model):
    dateTime = models.DateTimeField
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Change_Milestone(Event):
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE)


class Change_Comment(Event):
    pass


class Change_Code(Event):
    url = models.CharField(max_length=LENGTH_OF_FIELD)


class Label(models.Model):
    title = models.CharField(max_length=LENGTH_OF_FIELD)
    color = models.CharField(max_length=LENGTH_OF_FIELD)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
