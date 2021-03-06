# Generated by Django 3.0.2 on 2020-02-17 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('miniGithub', '0013_problem_current_assignee'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='problems',
            field=models.ManyToManyField(related_name='labels', to='miniGithub.Problem'),
        ),
        migrations.AddField(
            model_name='label',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='miniGithub.Project'),
        ),
    ]
