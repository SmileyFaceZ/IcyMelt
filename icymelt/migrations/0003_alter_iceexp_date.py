# Generated by Django 5.0.4 on 2024-04-21 17:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("icymelt", "0002_alter_iceexp_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="iceexp",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 4, 22, 0, 51, 29, 942258)
            ),
        ),
    ]
