# Generated by Django 5.0.1 on 2024-03-17 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0015_attendance_report_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="attendance_report",
            name="id",
        ),
        migrations.AlterField(
            model_name="attendance_report",
            name="attendance_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
