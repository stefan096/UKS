from enum import Enum

from django.db import models

# Create your models here.

LENGTH_OF_FIELD = 100
LENGTH_OF_FIELD_AREA = 500


class Project(models.Model):
    title = models.CharField(max_length=LENGTH_OF_FIELD)
    git_repo = models.CharField(max_length=LENGTH_OF_FIELD)


# class Problem(models.Model):
#     title = models.CharField(max_length=LENGTH_OF_FIELD)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
#     base_problem = models.ForeignKey('self', on_delete=models.CASCADE, null=True)


class Custom_User(models.Model):
    first_name = models.CharField(max_length=LENGTH_OF_FIELD)
    last_name = models.CharField(max_length=LENGTH_OF_FIELD)
    email = models.CharField(max_length=LENGTH_OF_FIELD)


class Custom_Event(models.Model):
    created_time = models.DateTimeField()
    creator = models.ForeignKey(Custom_User, on_delete=models.CASCADE, null=True)
    # problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)


# class Comment(Custom_Event):
#     description = models.CharField(max_length=LENGTH_OF_FIELD_AREA)


# class Problem_State(Enum):
#     OPEN = 1
#     CLOSED = 2
#
#
# class Change_State(Custom_Event):
#     new_state = models.CharField(
#       max_length=2,
#       choices=[(tag, tag.value) for tag in Problem_State]
#     )


# class Change_Assignee(Custom_Event):
#     assignee = models.ForeignKey(Custom_User, on_delete=models.CASCADE, null=True)


class Milestone(models.Model):
    dateTime = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)


# class Change_Milestone(Custom_Event):
#     milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, null=True)

#
# class Change_Comment(Custom_Event):
#     someField = models.CharField(max_length=LENGTH_OF_FIELD)


# class Change_Code(Custom_Event):
#     path_url = models.CharField(max_length=LENGTH_OF_FIELD)


class Label(models.Model):
    title = models.CharField(max_length=LENGTH_OF_FIELD)
    color = models.CharField(max_length=LENGTH_OF_FIELD)
    # problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)
