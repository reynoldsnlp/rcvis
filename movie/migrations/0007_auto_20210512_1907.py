# Generated by Django 3.0.8 on 2021-05-12 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0006_movie_giffile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='gifFile',
            field=models.FileField(blank=True, max_length=512, null=True, upload_to='gifs'),
        ),
    ]