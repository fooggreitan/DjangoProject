# Generated by Django 5.0.1 on 2024-04-04 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0027_alter_case_bitrix_staff_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Bitrix24",
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
                ("webhook", models.TextField()),
            ],
        ),
    ]
