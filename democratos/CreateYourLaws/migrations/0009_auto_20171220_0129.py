# Generated by Django 2.0 on 2017-12-20 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CreateYourLaws', '0008_auto_20171220_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cyl_user',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
    ]
