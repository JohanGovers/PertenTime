# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_timeentry_user_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeentry',
            name='submitted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
