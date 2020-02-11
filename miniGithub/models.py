from enum import Enum

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

# Create your models here.

LENGTH_OF_FIELD = 100
LENGTH_OF_FIELD_AREA = 500


class Problem_State(Enum):
    OPEN = 1
    CLOSED = 2


class Project(models.Model):
    title = models.CharField(max_length=LENGTH_OF_FIELD)
    git_repo = models.CharField(max_length=LENGTH_OF_FIELD)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    collaborators = models.ManyToManyField(User, related_name='collaborations')


class Milestone(models.Model):
    due_date = models.DateTimeField(null=True)
    created_time = models.DateTimeField(null=True)
    title = models.CharField(max_length=LENGTH_OF_FIELD, null=True)
    description = models.CharField(max_length=LENGTH_OF_FIELD_AREA, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)


class Problem(models.Model):
    title = models.CharField(max_length=LENGTH_OF_FIELD)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_time = models.DateTimeField(null=True)
    base_problem = models.ForeignKey('self', related_name='problem', on_delete=models.CASCADE, null=True, blank=True)
    linked_milestone = models.ForeignKey(Milestone, on_delete=models.SET_NULL, null=True)

    @classmethod
    def create(cls, title, description, project, owner):
        created_time = datetime.now()
        problem = cls(title=title, project=project, reported_by=owner, created_time=created_time)
        problem.save()
        comment = Comment.create(owner, description, problem)
        state = Change_State.create(owner, Problem_State['OPEN'].value, problem)
        return problem

    def close_problem(self, current_user):
        state = Change_State.create(current_user, Problem_State['CLOSED'].value, self)
        return self

    def reopen_problem(self, current_user):
        state = Change_State.create(current_user, Problem_State['OPEN'].value, self)
        return self

    def link_to_milestone(self, current_user, milestone):
        self.linked_milestone = milestone
        new_event = Change_Milestone.create(current_user, milestone, self)
        self.save()
        return self


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

    def edit(self, creator, description):
        edited_time = datetime.now()
        self.description = description
        self.save()
        Change_Comment.create(comment=self, created_time = edited_time, problem=self.problem, creator=creator)
        return self


class Change_Comment(Custom_Event):
    relatedComment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)

    @classmethod
    def create(cls, comment, created_time, problem, creator):
        comment_change = cls(creator=creator, problem=problem, relatedComment=comment, created_time=created_time)
        comment_change.save()
        return comment_change


class Change_State(Custom_Event):
    current_state = models.CharField(
      max_length=2,
      choices=[(tag, tag.value) for tag in Problem_State]
    )

    @classmethod
    def create(cls, creator, state, problem):
        created_time = datetime.now()
        new_state = cls(creator=creator, problem=problem, current_state=state, created_time=created_time)
        new_state.save()
        return new_state


# class Change_Assignee(Custom_Event):
#     assignee = models.ForeignKey(Custom_User, on_delete=models.CASCADE, null=True)


class Change_Milestone(Custom_Event):
    current_milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, null=True)

    @classmethod
    def create(cls, creator, milestone, problem):
        created_time = datetime.now()
        new_state = cls(creator=creator, problem=problem, current_milestone=milestone, created_time=created_time)
        new_state.save()
        return new_state


class Change_Code(models.Model):
    commit_url = models.CharField(max_length=LENGTH_OF_FIELD)
    commit_id = models.CharField(max_length=LENGTH_OF_FIELD)
    message = models.CharField(max_length=LENGTH_OF_FIELD)
    created_time = models.DateTimeField()
    creator = models.CharField(max_length=LENGTH_OF_FIELD)
    creator_email = models.CharField(max_length=LENGTH_OF_FIELD)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)

    @classmethod
    def create(cls, commit_url, commit_id, message, created_time, creator, creator_email, project):
        #created_time = datetime.now()
        new_state = cls(commit_url=commit_url, commit_id=commit_id, message=message, created_time=created_time,
                        creator=creator, creator_email=creator_email, project=project)
        new_state.save()
        return new_state


class Label(models.Model):
    title = models.CharField(max_length=LENGTH_OF_FIELD)
    color = models.CharField(max_length=LENGTH_OF_FIELD)
    # problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)
