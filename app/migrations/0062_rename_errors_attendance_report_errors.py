# Generated by Django 5.0.1 on 2024-05-02 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0061_rename_errors_attendance_report_errors_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="attendance_report",
            old_name="errors",
            new_name="Errors",
        ),
    ]
