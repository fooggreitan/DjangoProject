# Generated by Django 5.0.1 on 2024-04-22 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0048_alter_attendance_report_staff"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staff",
            name="address",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="staff",
            name="gender",
            field=models.CharField(max_length=108, null=True),
        ),
    ]
