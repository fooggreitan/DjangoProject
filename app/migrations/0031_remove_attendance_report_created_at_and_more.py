# Generated by Django 5.0.1 on 2024-03-17 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0030_attendance_report_staff_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="attendance_report",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="attendance_report",
            name="updated_at",
        ),
    ]
