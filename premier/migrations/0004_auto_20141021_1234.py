# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premier', '0003_auto_20141020_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='name_club',
            field=models.CharField(unique=True, max_length=63),
        ),
    ]
