# Generated by Django 4.0.3 on 2022-04-18 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_movie_number_visit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='number_visit',
            new_name='num_of_views',
        ),
    ]