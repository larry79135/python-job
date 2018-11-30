# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-09-28 11:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_book_publisher'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='publisher',
            field=models.ManyToManyField(to='index.Publisher', verbose_name='簽約出版社'),
        ),
    ]
