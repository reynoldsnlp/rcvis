# Generated by Django 3.0.8 on 2020-07-23 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextToSpeechCachedFile',
            fields=[
                ('text', models.CharField(max_length=512, primary_key=True, serialize=False, unique=True)),
                ('audioFile', models.FileField(upload_to='speech-synth')),
                ('lastUsed', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]