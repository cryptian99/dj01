# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('premier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id_player', models.AutoField(serialize=False, primary_key=True)),
                ('squad_number', models.IntegerField()),
                ('club_id', models.ForeignKey(verbose_name=b'id_club', to='premier.Club')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='club',
            name='id_club',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
