# Generated by Django 2.0.3 on 2018-04-20 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ezcook17', '0003_remove_postnew_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('amount', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.RemoveField(
            model_name='postnew',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='postnew',
            name='published_date',
        ),
    ]
