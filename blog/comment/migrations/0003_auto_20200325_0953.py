# Generated by Django 2.0 on 2020-03-25 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_auto_20200324_1128'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='nickname',
            new_name='author',
        ),
    ]
