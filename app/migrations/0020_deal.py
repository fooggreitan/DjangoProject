# Generated by Django 5.0.1 on 2024-04-02 22:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0019_remove_attendance_report_staff_id_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Deal",
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
                ("title", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("DATE_CREATE", models.DateTimeField()),
                ("DATE_MODIFY", models.DateTimeField()),
                ("Status", models.TextField()),
                ("CLOSEDATE", models.DateTimeField()),
                ("TYPE_ID", models.TextField()),
                (
                    "staff_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.staff"
                    ),
                ),
            ],
        ),
    ]
