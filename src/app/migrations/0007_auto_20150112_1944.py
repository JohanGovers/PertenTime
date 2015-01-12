# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_timeentry_submitted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeentry',
            name='submitted',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='submitted_until',
            field=models.DateField(default='2014-12-31'),
            preserve_default=False,
        ),
    ]
