from django.shortcuts import render, redirect
from app.models import Staff, Staff_Notification

def HOME(request):
    return render(request, 'Staff/home.html')


def NOTIFICATION(request):
    staff=Staff.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id
        notification = Staff_Notification.objects.filter(staff_id = staff_id)
        context = {
            'notification':notification,
        }
        return render(request, 'Staff/staff_notification.html', context)


def STATUSNOTIFICATION(request, status):
    notification=Staff_Notification.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect('staff_notification')