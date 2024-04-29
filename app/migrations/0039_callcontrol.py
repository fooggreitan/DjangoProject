# Generated by Django 5.0.1 on 2024-04-20 20:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0038_timecontrol"),
    ]

    operations = [
        migrations.CreateModel(
            name="callControl",
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
                ("CALL_TYPE", models.CharField(null=True)),
                ("CALL_FAILED_CODE", models.TextField(null=True)),
                ("PHONE_NUMBER", models.TextField(null=True)),
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
