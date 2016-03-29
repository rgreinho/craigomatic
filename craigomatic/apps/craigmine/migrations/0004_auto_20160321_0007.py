# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('craigmine', '0003_search_custom_search_args'), ]

    operations = [
        migrations.AlterField(model_name='search',
                              name='query',
                              field=models.CharField(default='',
                                                     max_length=300), ),
    ]
