# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150109_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeentry',
            name='user_profile',
            field=models.ForeignKey(default=1, to='app.UserProfile'),
            preserve_default=False,
        ),
    ]
