# Generated by Django 5.0.1 on 2024-05-02 18:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0065_callcontrol_id_call_taskcontrol_id_task_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance_report",
            name="staff",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                to_field="bitrix_staff_id",
            ),
        ),
    ]
