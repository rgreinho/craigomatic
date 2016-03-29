# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('craigmine', '0002_auto_20150526_0432'), ]

    operations = [
        migrations.AddField(model_name='search',
                            name='custom_search_args',
                            field=models.CharField(default='',
                                                   max_length=300), ),
    ]
