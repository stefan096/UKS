# Generated by Django 3.0.2 on 2020-02-22 23:23

from django.db import migrations, models
import miniGithub.models


class Migration(migrations.Migration):

    dependencies = [
        ('miniGithub', '0014_change_milestone_current_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change_milestone',
            name='current_state',
            field=models.CharField(choices=[(miniGithub.models.Milestone_State['OPEN'], 1), (miniGithub.models.Milestone_State['CLOSED'], 2)], max_length=2, null=True),
        ),
    ]
