# Generated by Django 5.0.1 on 2024-05-02 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0063_alter_taskcontrol_comment_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskcontrol",
            name="COMMENT",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="taskcontrol",
            name="CREATED_DATE",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="taskcontrol",
            name="DEADLINE",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="taskcontrol",
            name="DESCRIPTION",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="taskcontrol",
            name="GROUP_PROJECTS",
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name="taskcontrol",
            name="PRIORITY",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="taskcontrol",
            name="STATUS",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="taskcontrol",
            name="SUBSTATUS",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="taskcontrol",
            name="TASKOFCALL",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="taskcontrol",
            name="TITLE",
            field=models.TextField(null=True),
        ),
    ]
