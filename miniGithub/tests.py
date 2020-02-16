from django.test import TestCase
from django.contrib.auth.models import User
from miniGithub.models import Project, Problem, Problem_State

# Create your tests here.
class ModelTests(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='user', email='user@test.com', password='password')
    self.project = Project.objects.create(title="Test project", git_repo="https://github.com/stefan096/UKS", owner=self.user)
    self.problem = Problem.create("Problem test", "Problem description test", self.project, self.user)

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
