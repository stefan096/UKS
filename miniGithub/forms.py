from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100)


class ProblemForm(forms.Form):
    title = forms.CharField(max_length=100, help_text="Problem title")
    description = forms.CharField(max_length=500, help_text="Problem description")


class EditCommentForm(forms.Form):
    description = forms.CharField(max_length=500, help_text="Comment description",
            widget=forms.Textarea(attrs={'class': "form-control"}),
)


class MilestoneForm(forms.Form):
    title = forms.CharField(max_length=100, help_text="Milestone title")
    description = forms.CharField(max_length=500, help_text="Milestone description", required=False)
    due_date = forms.DateTimeField()

    def method_to_construct(self, milestone):
        self.title = milestone.title
        self.description = milestone.description
        self.due_date = milestone.due_date

class LabelForm(forms.Form):
    title = forms.CharField(max_length=100, help_text="Label title")
    color = forms.CharField(max_length=100, help_text="Label color")

    def method_to_construct(self, label):
        self.title = label.title
        self.color = label.color