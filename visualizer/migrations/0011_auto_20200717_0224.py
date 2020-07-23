# Generated by Django 3.0.8 on 2020-07-17 02:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('visualizer', '0010_jsonconfig_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoMovie',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('generatedOnApplicationVersion',
                 models.CharField(
                     max_length=30)),
                ('movieFile',
                 models.FileField(
                     upload_to='movies')),
                ('resolutionWidth',
                 models.PositiveIntegerField(
                     validators=[
                         django.core.validators.MinValueValidator(1),
                         django.core.validators.MaxValueValidator(1920)])),
                ('resolutionHeight',
                 models.PositiveIntegerField(
                     validators=[
                         django.core.validators.MinValueValidator(1),
                         django.core.validators.MaxValueValidator(1920)])),
            ],
        ),
        migrations.AddField(
            model_name='jsonconfig',
            name='isVideoGenerationInProgress',
            field=models.BooleanField(
                default=False),
        ),
        migrations.AddField(
            model_name='jsonconfig',
            name='movieHorizontal',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='visualizer.AutoMovie'),
        ),
        migrations.AddField(
            model_name='jsonconfig',
            name='movieVertical',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='+',
                to='visualizer.AutoMovie'),
        ),
    ]