# Generated by Django 3.1.7 on 2021-03-10 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210305_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo_url',
            field=models.ImageField(unique=True, upload_to='img'),
        ),
    ]
