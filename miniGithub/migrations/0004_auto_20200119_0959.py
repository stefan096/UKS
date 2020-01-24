# Generated by Django 3.0.2 on 2020-01-19 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('miniGithub', '0003_auto_20200119_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='base_problem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='problem', to='miniGithub.Problem'),
        ),
    ]