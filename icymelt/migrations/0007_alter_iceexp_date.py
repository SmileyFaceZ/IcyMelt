# Generated by Django 4.2.11 on 2024-05-10 17:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("icymelt", "0006_alter_iceexp_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="iceexp",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 5, 11, 0, 5, 32, 917076)
            ),
        ),
    ]
