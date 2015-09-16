# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('iso_639_3', models.CharField(unique=True, max_length=3, verbose_name='ISO 639-3')),
                ('iso_639_1', models.CharField(unique=True, null=True, max_length=2, blank=True, verbose_name='ISO 639-1')),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
            ],
            options={
                'ordering': ['iso_639_3'],
            },
        ),
    ]
