# Generated by Django 2.2 on 2019-06-22 18:24

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JsonConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jsonFile', models.FileField(upload_to='')),
                ('slug', models.SlugField(unique=True)),
                ('uploadedAt', models.DateTimeField(auto_now_add=True)),
                ('hideTransferlessRounds', models.BooleanField(default=False)),
                ('hideDecimals', models.BooleanField(default=False)),
                ('rotateNames', models.BooleanField(default=False)),
            ],
        ),
    ]
