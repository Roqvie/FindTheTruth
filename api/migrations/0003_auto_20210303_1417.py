# Generated by Django 3.1.7 on 2021-03-03 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210301_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(unique=True, upload_to='images'),
        ),
    ]
