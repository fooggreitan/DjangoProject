# Generated by Django 5.0.1 on 2024-04-03 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0022_customuser_bitrix_staff_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="deal",
            name="staff_id",
        ),
        migrations.AddField(
            model_name="deal",
            name="bitrix_staff_id",
            field=models.CharField(null=True),
        ),
    ]