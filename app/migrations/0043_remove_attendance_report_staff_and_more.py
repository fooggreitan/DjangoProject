# Generated by Django 5.0.1 on 2024-04-21 23:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0042_taskcontrol_created_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="attendance_report",
            name="staff",
        ),
        migrations.AddField(
            model_name="attendance_report",
            name="staff_id",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
