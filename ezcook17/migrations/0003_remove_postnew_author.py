# Generated by Django 2.0.3 on 2018-03-18 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ezcook17', '0002_postnew'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postnew',
            name='author',
        ),
    ]
