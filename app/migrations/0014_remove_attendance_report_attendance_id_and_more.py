# Generated by Django 5.0.1 on 2024-03-18 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0013_remove_staff_notification_created_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="attendance_report",
            name="attendance_id",
        ),
        migrations.RemoveField(
            model_name="attendance_report",
            name="staff_id",
        ),
        migrations.RemoveField(
            model_name="attendance_report",
            name="task_id",
        ),
        migrations.AddField(
            model_name="attendance_report",
            name="name_report",
            field=models.TextField(default="qewq"),
            preserve_default=False,
        ),
    ]
