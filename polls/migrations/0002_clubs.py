# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clubs',
            fields=[
                ('id_club', models.IntegerField(serialize=False, primary_key=True)),
                ('name_club', models.CharField(max_length=63)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
