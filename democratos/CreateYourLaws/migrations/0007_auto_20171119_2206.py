# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 22:06
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CreateYourLaws', '0006_auto_20170625_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='LawProp',
            fields=[
                ('lawarticle_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='CreateYourLaws.LawArticle')),
                ('details', ckeditor.fields.RichTextField()),
            ],
            options={
                'ordering': ['-approval_factor', '-update'],
                'abstract': False,
            },
            bases=('CreateYourLaws.lawarticle',),
        ),
        migrations.AddField(
            model_name='proposition',
            name='details',
            field=ckeditor.fields.RichTextField(default=' '),
            preserve_default=False,
        ),
    ]
