# Generated by Django 3.2.12 on 2022-03-23 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0015_auto_20220322_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='thumbimage',
            field=models.ImageField(default=None, upload_to='', verbose_name='缩略图路径'),
        ),
    ]
