# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-28 11:41
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20160828_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookborrow',
            name='date_borrow_end',
            field=models.DateField(default=datetime.datetime(2016, 8, 28, 11, 41, 1, 821254, tzinfo=utc)),
            preserve_default=False,
        ),
    ]