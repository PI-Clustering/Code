# Generated by Django 3.1.7 on 2021-09-18 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webApp', '0003_auto_20210918_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='ISBN',
            field=models.BigIntegerField(blank=True, default=0),
        ),
    ]
