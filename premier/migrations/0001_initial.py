# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id_club', models.IntegerField(serialize=False, primary_key=True)),
                ('name_club', models.CharField(max_length=63)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
