import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Customer(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.name)

class CustomUser(AbstractUser):
    USER = (
        (1, 'HOD'),
        (2, 'STAFF'),
        (3, 'STUDENT'),
    )
    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')

class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=108)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.username

class Staff_Notification(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.staff_id.admin.first_name

class Task(models.Model):
    task = models.TextField()
    gender = models.CharField(max_length=108)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task

# class Attendance(models.Model):
#     staff_id = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
#     task_id = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
#     attendance_data = models.DateTimeField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.staff_id.name

class Attendance_Report(models.Model):
    staff_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name_report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.staff_id
    # def get_absolute_url(self):
    #     return reverse('post_datail', kwargs={"slug": self.slug})