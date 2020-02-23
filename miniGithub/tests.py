from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from miniGithub.models import Project, Problem, Problem_State, Milestone, Milestone_State, Change_State


# Create your tests here.
class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', email='user@test.com', password='password')
        self.project = Project.objects.create(title="Test project", git_repo="https://github.com/stefan096/UKS",
                                              owner=self.user)
        self.problem = Problem.create("Problem test", "Problem description test", self.project, self.user)
        self.currentTime = datetime.now()
        self.dueTime = datetime.now()
        self.milestone = Milestone.create(self.dueTime, self.currentTime, "Milestone1", "Ovo je opis za milestone 1",
                                          self.project)
        #self.milestone.due_date = self.dueTime
        # self.milestone.created_time = self.currentTime
        # self.milestone.title = "Milestone1"
        # self.milestone.description = "Ovo je opis za milestone 1"
        # self.milestone.project = self.project

    def test_problem_creation_comment(self):
        problem = Problem.create("Problem title", "Problem description", self.project, self.user)
        self.assertEqual(problem.title, "Problem title")
        related_comments = problem.get_comments()
        self.assertEqual(related_comments.count(), 1)
        self.assertEqual(related_comments.last().description, "Problem description")
        state_changes = self.problem.get_state_changes()
        self.assertEqual(state_changes.count(), 1)
        self.assertEqual(int(state_changes.last().current_state), Problem_State['OPEN'].value)

    def test_problem_closing_reopening(self):
        self.problem.close_problem(self.user)
        state_changes = self.problem.get_state_changes()
        self.assertEqual(state_changes.count(), 2)
        self.assertEqual(int(state_changes.last().current_state), Problem_State['CLOSED'].value)
        self.problem.reopen_problem(self.user)
        state_changes = self.problem.get_state_changes()
        self.assertEqual(state_changes.count(), 3)
        self.assertEqual(int(state_changes.last().current_state), Problem_State['OPEN'].value)

    def test_problem_assign_user(self):
        assignee = User.objects.create_user(username='assignee', email='assignee@test.com', password='password')
        problem = self.problem.assign_user(self.user, assignee)
        self.assertEqual(problem.current_assignee, assignee)
        assignee_changes = problem.get_assignee_changes()
        self.assertEqual(assignee_changes.count(), 1)
        self.assertEqual(assignee_changes.last().assignee, assignee)

    def test_creating_milestone(self):
        milestone = Milestone.create(self.dueTime, self.currentTime, "Milestone1", "Ovo je opis za milestone 1",
                                     self.project)
        self.assertEqual(milestone.due_date, self.dueTime)
        self.assertEqual(milestone.created_time, self.currentTime)
        self.assertEqual(milestone.title, "Milestone1")
        self.assertEqual(milestone.description, "Ovo je opis za milestone 1")
        self.assertEqual(milestone.project, self.project)

    def test_linking_milestone_to_problem(self):
        problem = self.problem.link_to_milestone(self.user, self.milestone)
        self.assertEqual(problem.linked_milestone, self.milestone)
        self.assertEqual(problem.reported_by, self.user)

    def test_open_milestone(self):
        self.milestone.open_milestone(self.user)
        state_changes = Change_State.objects.filter(problem=self.problem.id)
        self.assertEqual(int(state_changes.last().current_state), Milestone_State['OPEN'].value)
        self.assertEqual(state_changes.last().creator, self.user)
        self.assertEqual(state_changes.last().problem, self.problem)

    def test_close_milestone(self):
        self.milestone.close_milestone_problem(self.user, self.problem)
        state_changes = Change_State.objects.filter(problem=self.problem)
        self.assertEqual(int(state_changes.last().current_state), 1)
        self.assertEqual(state_changes.last().creator, self.user)
        self.assertEqual(state_changes.last().problem, self.problem)
