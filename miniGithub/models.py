from enum import Enum

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

# Create your models here.

LENGTH_OF_FIELD = 100
LENGTH_OF_FIELD_AREA = 500


class Project(models.Model):
    title = models.CharField(max_length=LENGTH_OF_FIELD)
    git_repo = models.CharField(max_length=LENGTH_OF_FIELD)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    collaborators = models.ManyToManyField(User, related_name='collaborations')


class Problem(models.Model):
    title = models.CharField(max_length=LENGTH_OF_FIELD)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    base_problem = models.ForeignKey('self', related_name='problem', on_delete=models.CASCADE, null=True, blank=True)
    
    @classmethod
    def create(cls, title, description, project, owner):
        problem = cls(title=title, project=project)
        problem.save()
        comment = Comment.create(owner, description, problem)
        return problem


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=LENGTH_OF_FIELD)
    last_name = models.CharField(max_length=LENGTH_OF_FIELD)
    email = models.EmailField(max_length=LENGTH_OF_FIELD)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Custom_Event(models.Model):
    created_time = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)


class Comment(Custom_Event):
    description = models.CharField(max_length=LENGTH_OF_FIELD_AREA)
    @classmethod
    def create(cls, creator, description, problem):
        created_time = datetime.now()
        comment = cls(creator=creator, problem=problem, description=description, created_time=created_time)
        comment.save()
        return comment


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


# class Change_Comment(Custom_Event):
#     someField = models.CharField(max_length=LENGTH_OF_FIELD)


# class Change_Code(Custom_Event):
#     path_url = models.CharField(max_length=LENGTH_OF_FIELD)


class Label(models.Model):
    title = models.CharField(max_length=LENGTH_OF_FIELD)
    color = models.CharField(max_length=LENGTH_OF_FIELD)
    # problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)
