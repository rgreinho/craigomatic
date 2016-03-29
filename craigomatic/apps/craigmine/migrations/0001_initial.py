# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(name='Item',
                               fields=[
                                   ('retrieved', models.DateTimeField(auto_created=True)),
                                   ('id', models.CharField(max_length=200,
                                                           serialize=False,
                                                           primary_key=True)),
                                   ('link', models.URLField()),
                                   ('post_date', models.DateTimeField()),
                                   ('pnr', models.CharField(max_length=200)),
                                   ('price', models.PositiveIntegerField()),
                                   ('title', models.CharField(max_length=200)),
                               ], ),
        migrations.CreateModel(name='Search',
                               fields=[
                                   ('id', models.AutoField(auto_created=True,
                                                           verbose_name='ID',
                                                           serialize=False,
                                                           primary_key=True)),
                                   ('server', models.CharField(max_length=200)),
                                   ('category', models.CharField(max_length=50)),
                                   ('has_pic', models.BooleanField(default=True)),
                                   ('min_ask', models.PositiveIntegerField(default=0)),
                                   ('max_ask', models.PositiveIntegerField(default=1000)),
                                   ('query', models.CharField(max_length=300)),
                                   ('tag', models.CharField(max_length=20)),
                                   ('last_update', models.DateTimeField(auto_now=True)),
                               ], ),
        migrations.AddField(model_name='item',
                            name='search',
                            field=models.ForeignKey(to='craigmine.Search'), ),
    ]
