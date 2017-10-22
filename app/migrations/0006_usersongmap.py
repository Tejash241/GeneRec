# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-22 09:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_song'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSongMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Song')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.UserProfile')),
            ],
        ),
    ]
