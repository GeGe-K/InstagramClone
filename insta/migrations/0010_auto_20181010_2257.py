# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-10 19:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0009_auto_20181010_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
