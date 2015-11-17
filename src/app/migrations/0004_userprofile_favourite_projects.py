# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_userprofile_skip_confirm_submit_dialog'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='favourite_projects',
            field=models.ManyToManyField(to='app.Project'),
            preserve_default=True,
        ),
    ]
