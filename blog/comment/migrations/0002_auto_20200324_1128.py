# Generated by Django 2.0 on 2020-03-24 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='target',
            field=models.CharField(max_length=500, verbose_name='评论目标'),
        ),
    ]