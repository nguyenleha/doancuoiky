# Generated by Django 3.2.5 on 2021-08-16 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_alter_profile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.BigIntegerField(blank=True, max_length=10, null=True),
        ),
    ]
