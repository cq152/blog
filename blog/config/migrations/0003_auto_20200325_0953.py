# Generated by Django 2.0 on 2020-03-25 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_auto_20200324_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sidepane',
            name='type',
            field=models.PositiveIntegerField(choices=[(0, '每日一句'), (1, '最热文章'), (2, '最新文章'), (3, '最新评论')], default=0, verbose_name='文章类型'),
        ),
    ]
