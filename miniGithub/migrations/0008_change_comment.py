# Generated by Django 3.0.2 on 2020-01-31 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('miniGithub', '0007_auto_20200128_2111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Change_Comment',
            fields=[
                ('custom_event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='miniGithub.Custom_Event')),
                ('relatedComment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='miniGithub.Comment')),
            ],
            bases=('miniGithub.custom_event',),
        ),
    ]
