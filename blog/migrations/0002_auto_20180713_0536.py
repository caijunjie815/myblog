# Generated by Django 2.0.7 on 2018-07-13 05:36

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Article',
            new_name='Post',
        ),
    ]
