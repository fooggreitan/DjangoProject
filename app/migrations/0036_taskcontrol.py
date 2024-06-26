# Generated by Django 5.0.1 on 2024-04-09 17:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0035_alter_deal_bitrix_staff_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="TaskControl",
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
                ("TITLE", models.TextField()),
                ("DESCRIPTION", models.TextField()),
                ("PRIORITY", models.TextField()),
                ("STATUS", models.TextField()),
                ("SUBSTATUS", models.TextField()),
                ("DEADLINE", models.DateTimeField()),
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
