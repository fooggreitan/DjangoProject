# Generated by Django 5.0.1 on 2024-04-21 23:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0045_alter_attendance_report_staff"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance_report",
            name="staff",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
