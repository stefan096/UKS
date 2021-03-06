# Generated by Django 3.0.2 on 2020-01-19 09:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('miniGithub', '0002_project_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('custom_event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='miniGithub.Custom_Event')),
                ('description', models.CharField(max_length=500)),
            ],
            bases=('miniGithub.custom_event',),
        ),
        migrations.AlterField(
            model_name='custom_event',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('base_problem', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='problem', to='miniGithub.Problem')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='miniGithub.Project')),
            ],
        ),
        migrations.AddField(
            model_name='custom_event',
            name='problem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='miniGithub.Problem'),
        ),
    ]
