# Generated by Django 3.2.12 on 2022-03-22 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0013_alter_userinfo_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='phone',
            field=models.IntegerField(default=0, unique=True, verbose_name='电话'),
        ),
    ]