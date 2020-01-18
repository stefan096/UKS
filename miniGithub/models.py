from enum import Enum

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

LENGTH_OF_FIELD = 100
LENGTH_OF_FIELD_AREA = 500


class Project(models.Model):
    title = models.CharField(max_length=LENGTH_OF_FIELD)
    git_repo = models.CharField(max_length=LENGTH_OF_FIELD)


class Problem(models.Model):
    title = models.CharField(max_length=LENGTH_OF_FIELD)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    base_problem = models.ForeignKey('self', on_delete=models.CASCADE, null=True)


class Profile(models.Model):
    first_name = models.CharField(max_length=LENGTH_OF_FIELD)
    last_name = models.CharField(max_length=LENGTH_OF_FIELD)
    email = models.CharField(max_length=LENGTH_OF_FIELD)


# user = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username
#
#
# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         Custom_User.objects.create(user=instance)
#     instance.profile.save()


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100, blank=True)
#     last_name = models.CharField(max_length=100, blank=True)
#     email = models.EmailField(max_length=150)
#     bio = models.TextField()
#
#     def __str__(self):
#         return self.user.username

class Custom_Event(models.Model):
    created_time: models.DateTimeField
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)


class Comment(Custom_Event):
    description: models.CharField(max_length=LENGTH_OF_FIELD_AREA)


class Problem_State(Enum):
    OPEN = 1
    CLOSED = 2


class Change_State(Custom_Event):
    new_state: models.CharField(
      max_length=2,
      choices=[(tag, tag.value) for tag in Problem_State]
    )


class Change_Assignee(Custom_Event):
    assignee = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)


class Milestone(models.Model):
    dateTime = models.DateTimeField
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)


class Change_Milestone(Custom_Event):
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, null=True)


class Change_Comment(Custom_Event):
    someField = models.ForeignKey(Milestone, on_delete=models.CASCADE, null=True)
    pass


class Change_Code(Custom_Event):
    pass


class Label(models.Model):
    title = models.CharField(max_length=LENGTH_OF_FIELD)
    color = models.CharField(max_length=LENGTH_OF_FIELD)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)

