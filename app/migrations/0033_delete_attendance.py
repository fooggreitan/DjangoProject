# Generated by Django 5.0.1 on 2024-03-17 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0032_attendance_report_created_at_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Attendance",
        ),
    ]
