# Generated by Django 2.0 on 2020-03-03 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20200302_1125'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='summmary',
            new_name='summary',
        ),
    ]