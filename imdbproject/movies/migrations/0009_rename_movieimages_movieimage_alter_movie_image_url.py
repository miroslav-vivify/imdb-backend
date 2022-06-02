# Generated by Django 4.0.3 on 2022-05-20 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_merge_20220520_0727'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MovieImages',
            new_name='MovieImage',
        ),
        migrations.AlterField(
            model_name='movie',
            name='image_url',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.movieimage'),
        ),
    ]
