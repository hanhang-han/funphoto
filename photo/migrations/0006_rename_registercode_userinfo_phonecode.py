# Generated by Django 3.2.12 on 2022-03-15 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0005_userinfo_registercode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='registercode',
            new_name='phonecode',
        ),
    ]
