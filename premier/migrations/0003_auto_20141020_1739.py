# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premier', '0002_auto_20141020_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='aliases',
            field=models.CharField(default=None, max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='given_name',
            field=models.CharField(default=None, max_length=63),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='surname',
            field=models.CharField(default=None, max_length=63),
            preserve_default=True,
        ),
    ]
