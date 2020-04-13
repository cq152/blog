# Generated by Django 2.0 on 2020-04-11 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0004_link_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='sidepane',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
    ]
