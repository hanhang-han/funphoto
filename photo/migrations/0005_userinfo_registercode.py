# Generated by Django 3.2.12 on 2022-03-15 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0004_alter_userinfo_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='registercode',
            field=models.IntegerField(null=True, verbose_name='短信验证码'),
        ),
    ]
