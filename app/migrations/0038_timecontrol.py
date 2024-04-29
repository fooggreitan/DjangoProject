# Generated by Django 5.0.1 on 2024-04-20 10:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0037_taskcontrol_time_estimate"),
    ]

    operations = [
        migrations.CreateModel(
            name="TimeControl",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("DURATION", models.DurationField(null=True)),
                ("TIME_LEAKS", models.DurationField(null=True)),
                ("STATUS", models.TextField()),
                ("START_TIME", models.DateTimeField(null=True)),
                ("END_TIME", models.DateTimeField(null=True)),
                (
                    "bitrix_staff_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        to_field="bitrix_staff_id",
                    ),
                ),
            ],
        ),
    ]
