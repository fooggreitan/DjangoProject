from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

class UserModel(UserAdmin):
    list_display = ['username', 'user_type']

admin.site.register(CustomUser, UserModel)
admin.site.register(Staff)
admin.site.register(Task)
admin.site.register(Attendance)
admin.site.register(Attendance_Report)
admin.site.register(Staff_Notification)

