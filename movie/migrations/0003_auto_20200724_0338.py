# Generated by Django 3.0.8 on 2020-07-24 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_texttospeechcachedfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='texttospeechcachedfile',
            name='audioFile',
            field=models.FileField(max_length=512, upload_to='speech-synth'),
        ),
        migrations.AlterField(
            model_name='texttospeechcachedfile',
            name='text',
            field=models.CharField(max_length=2048, primary_key=True, serialize=False, unique=True),
        ),
    ]
