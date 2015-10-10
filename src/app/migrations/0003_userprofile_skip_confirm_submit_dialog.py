# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20150218_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='skip_confirm_submit_dialog',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
