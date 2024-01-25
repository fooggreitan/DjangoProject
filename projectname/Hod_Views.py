from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import CustomUser, Staff, Task, Staff_Notification
from django.contrib import messages

@login_required(login_url='/')
def HOME(request):
    staff_count = Staff.objects.all().count()

    staff_male = Staff.objects.filter(gender = 'Male').count()
    staff_female = Staff.objects.filter(gender = 'Female').count()

    context = {
        'staff_count': staff_count,
        'staff_male': staff_male,
        'staff_female': staff_female,
    }

    return render(request, 'Hod/home.html', context)

@login_required(login_url='/')
def ADD_STAFF(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email Is Already Taken ! ')
            return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username Is Already Taken ! ')
            return redirect('add_staff')
        else:
            user = CustomUser(
                profile_pic = profile_pic,
                first_name = first_name,
                last_name= last_name,
                email=email,
                user_type = 2,
                username = username
            )
            user.set_password(password)
            user.save()

            staff = Staff(
                admin = user,
                address = address,
                gender = gender,
            )
            staff.save()
            messages.success(request, user.first_name + " " + user.last_name + "Персонал создан!")
            return redirect('add_staff')
    return render(request, 'Hod/add_staff.html')

@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()
    context = {
        'staff': staff,
    }
    return render(request, 'Hod/view_staff.html', context)

@login_required(login_url='/')
def EDIT_STAFF(request, id):
    staff = Staff.objects.get(id=id)
    context = {
        'staff':staff,
    }
    return render(request, 'Hod/edit_staff.html', context)

@login_required(login_url='/')
def DELETE_STAFF(request, admin):
    staff = CustomUser.objects.get(id=admin)
    staff.delete()
    messages.success(request, "Успешно удален!")
    return redirect('view_staff')

@login_required(login_url='/')
def VIEW_TASK(request):

    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all().order_by('-id')[0:5]
    context = {
        'staff': staff,
        'see_notification': see_notification
    }
    return render(request, 'Hod/view_task.html', context)

@login_required(login_url='/')
def VIEW_ATT(request):
    return render(request, 'Hod/view_attendance.html')

def STAFF_SEND_NOTIFICATION(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all().order_by('-id')[0:5]
    context = {
        'staff': staff,
        'see_notification': see_notification
    }
    return render(request, 'Hod/staff_send_notification.html', context)


def STAFF_SAVE_NOTIFICATION(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        message=request.POST.get('message')

        staff = Staff.objects.get(admin = staff_id)
        notification = Staff_Notification(
            staff_id = staff,
            message = message,
        )
        notification.save()
        messages.success(request, 'Всё отправлено')
    return redirect('staff_send_notification')


def ABOUT_PROFILE(request):
    staff = Staff.objects.all()
    context = {
        'staff': staff,
    }
    return render(request, 'Hod/about_profile.html', context)


def VIEW_STAFF_TASK(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all().order_by('-id')
    context = {
        'staff': staff,
        'see_notification': see_notification
    }
    return render(request, 'Staff/view_task.html', context)