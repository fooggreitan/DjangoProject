from django.db import models
from django.contrib.auth.models import AbstractUser
from django_pandas.managers import DataFrameManager

class CustomUser(AbstractUser):
    USER = (
        (1, 'HOD'),
        (2, 'STAFF'),
        (3, 'STUDENT'),
    )
    user_type = models.CharField(choices=USER, max_length=50, default=1)
    WORK_POSITION = models.TextField(null=True)
    WORK_DEPARTMENT = models.TextField(null=True)
    profile_pic = models.ImageField(upload_to='media/profile_pic', null=True)
    bitrix_staff_id = models.CharField(null=True, unique=True)

class Customer(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class Staff(models.Model):
    address = models.TextField(null=True)
    gender = models.CharField(max_length=108, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    admin = models.OneToOneField(
        CustomUser,
        unique=False,
        to_field='bitrix_staff_id',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.admin.username

class Deal(models.Model):
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    DATE_CREATE = models.DateTimeField()
    DATE_MODIFY = models.DateTimeField()
    Status = models.TextField()
    CLOSEDATE = models.DateTimeField()
    TYPE_ID = models.TextField()

    bitrix_staff_id = models.ForeignKey(
        CustomUser,
        unique=False,
        to_field='bitrix_staff_id',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.title

class Bitrix24(models.Model):
    name_webhook = models.TextField(default='one')
    webhook = models.TextField()
    def __str__(self):
        return self.webhook

class Case(models.Model):
    DESCRIPTION = models.TextField()
    CREATED = models.DateTimeField()
    LAST_UPDATED = models.DateTimeField()
    COMPLETED = models.TextField()
    START_TIME = models.DateTimeField(null=True)
    END_TIME = models.DateTimeField(null=True)
    DEADLINE = models.DateTimeField()

    bitrix_staff_id = models.ForeignKey(
        CustomUser,
        unique=False,
        to_field='bitrix_staff_id',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.DESCRIPTION

class Staff_Notification(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.staff_id.admin.first_name

class TaskControl(models.Model):
    TITLE = models.TextField(null=True)
    DESCRIPTION = models.TextField(null=True)
    PRIORITY = models.TextField(null=True)
    STATUS = models.TextField(null=True)
    SUBSTATUS = models.TextField(null=True)
    DEADLINE = models.DateTimeField(null=True)
    TIME_ESTIMATE = models.TextField(null=True, default=0)
    CREATED_DATE = models.DateTimeField(null=True)
    GROUP_PROJECTS = models.CharField(null=True)

    bitrix_staff_id = models.ForeignKey(
        CustomUser,
        unique=False,
        to_field='bitrix_staff_id',
        on_delete=models.CASCADE,
        null=True
    )
    def __str__(self):
        return self.TITLE

class callControl(models.Model):
    DURATION = models.DurationField(null=True)
    CALL_TYPE = models.CharField(null=True)
    CALL_FAILED_CODE = models.TextField(null=True)
    PHONE_NUMBER = models.TextField(null=True)
    DateCreate = models.DateTimeField(null=True)
    VOTE = models.TextField(null=True)
    COST = models.TextField(null=True)

    bitrix_staff_id = models.ForeignKey(
        CustomUser,
        unique=False,
        to_field='bitrix_staff_id',
        on_delete=models.CASCADE,
        null=True
    )
    objects = DataFrameManager()
    def __str__(self):
        return self.bitrix_staff_id

class TimeControl(models.Model):
    bitrix_staff_id = models.ForeignKey(
        CustomUser,
        unique=False,
        to_field='bitrix_staff_id',
        on_delete=models.CASCADE,
        null=True
    )
    DURATION = models.DurationField(null=True)
    TIME_LEAKS = models.DurationField(null=True)
    STATUS = models.TextField()

    START_TIME = models.DateTimeField(null=True)
    END_TIME = models.DateTimeField(null=True)

    def __str__(self):
        return self.bitrix_staff_id

class Task(models.Model):
    task = models.TextField()
    gender = models.CharField(max_length=108)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task

class Attendance(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
    task_id = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    attendance_data = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.staff_id.name

class Attendance_Report(models.Model):
    # staff_id = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
    # task_id = models.ForeignKey(Task, on_delete=models.DO_NOTHING)

    # new_id = models.ForeignKey (Staff, on_delete=models.DO_NOTHING, primary_key=True, unique=True)

    name_report = models.CharField(max_length=200)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    progress = models.TextField(null=True)
    Errors = models.TextField(null=True)
    practices_improving_your = models.TextField(null=True)
    performance = models.TextField(null=True)
    general_comment = models.TextField(null=True)
    possible_risks = models.TextField(null=True)

    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name_report