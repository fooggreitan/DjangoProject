# Generated by Django 5.0.1 on 2024-01-25 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0009_staff_notification_email_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="staff_notification",
            name="email",
        ),
        migrations.RemoveField(
            model_name="staff_notification",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="staff_notification",
            name="last_name",
        ),
        migrations.RemoveField(
            model_name="staff_notification",
            name="profile_pic",
        ),
    ]
