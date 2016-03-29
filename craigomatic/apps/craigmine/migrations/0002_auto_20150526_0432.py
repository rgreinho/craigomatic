# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [('craigmine', '0001_initial'), ]

    operations = [
        migrations.AlterField(model_name='item',
                              name='retrieved',
                              field=models.DateTimeField(auto_now_add=True), ),
    ]
