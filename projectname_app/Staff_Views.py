from django.shortcuts import render, redirect
from app.models import Staff, Staff_Notification
from django.contrib.auth.decorators import login_required
from app.models import CustomUser, Staff, Case, Task, TimeControl, Staff_Notification, Attendance_Report, Deal, Bitrix24, callControl, TaskControl
from datetime import datetime
from datetime import timedelta
from fast_bitrix24 import Bitrix
from django.conf import settings
from django.db.models import Count, IntegerField, Sum
from django.db.models.functions import ExtractMonth


@login_required(login_url='/')
def HOME(request):
    call_count = callControl.objects.filter(bitrix_staff_id=request.user.bitrix_staff_id).count()
    task_count = TaskControl.objects.filter(bitrix_staff_id=request.user.bitrix_staff_id ).count()

    months_of_interest = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

    calls = callControl.objects.filter(bitrix_staff_id=request.user.bitrix_staff_id, DateCreate__year=datetime.now().year)
    task = TaskControl.objects.filter(bitrix_staff_id=request.user.bitrix_staff_id, CREATED_DATE__year=datetime.now().year)
    time_sum = (TimeControl.objects.filter(bitrix_staff_id=request.user.bitrix_staff_id, START_TIME__year=datetime.now().year).values('DURATION').aggregate(total_duration=Sum('DURATION'))['total_duration'] or timedelta(seconds=0)).total_seconds()
    time_sum = time_sum / 3600

    monthly_calls = {}
    monthly_task = {}
    monthly_task_e = {}
    monthly_calls_e = {}

    for month_name in months_of_interest:
        month_number = datetime.strptime(month_name, "%B").month
        calls_less_30 = calls.filter(DURATION__lt='30', DateCreate__month=month_number).count()
        calls_more_5 = calls.filter(DURATION__gt='300', DateCreate__month=month_number).count()
        calls_normal = calls.filter(DURATION__lt='300', DURATION__gt='30', DateCreate__month=month_number).count()
        monthly_calls[month_name] = {
            'total_calls_less_30': calls_less_30,
            'total_calls_more_5': calls_more_5,
            'total_calls_normal': calls_normal,
        }

    for month_name in months_of_interest:
        month_number = datetime.strptime(month_name, "%B").month
        completed_count = task.filter(STATUS='5', CREATED_DATE__month=month_number).count()
        overdue_task = task.filter(SUBSTATUS='-1', CREATED_DATE__month=month_number).count()
        monthly_task_e[month_name] = {
            'overdue_task': overdue_task,
            'completed_count': completed_count
        }

    for month_name in months_of_interest:
        month_number = datetime.strptime(month_name, "%B").month
        successful_calls = calls.filter(CALL_FAILED_CODE='200', DateCreate__month=month_number).count()
        monthly_calls_e[month_name] = {
            'successful_calls': successful_calls,
        }

    for month_name in months_of_interest:
        month_number = datetime.strptime(month_name, "%B").month
        needs_rework_count = task.filter(STATUS='7', CREATED_DATE__month=month_number).count()
        monthly_task[month_name] = {
            'needs_rework_count': needs_rework_count,
        }

    users = CustomUser.objects.filter(user_type=2)
    if Bitrix24.objects.get(name_webhook='one').webhook == '':
        redirect('hod_home')
    else:
        webhook = Bitrix(Bitrix24.objects.get(name_webhook='one').webhook)

        '''Звонки'''

        call_values = [{k: v for k, v in d.items() if k in
                        ['ID', 'PORTAL_USER_ID', 'CALL_TYPE', 'PHONE_NUMBER', 'CALL_DURATION', 'CALL_START_DATE',
                         'CALL_FAILED_CODE', 'COMMENT']} for d in
                       webhook.get_all('voximplant.statistic.get')]

        for call in call_values:
            user_id = call.get('PORTAL_USER_ID')
            print(user_id)
            try:
                user = callControl.objects.filter(ID_CALL=call.get('ID'))

                if user.exists():
                    user = user.first()
                    user.PHONE_NUMBER = call.get('PHONE_NUMBER')
                    user.DURATION = '{:02}:{:02}:{:02}'.format(int(call.get('CALL_DURATION')) // 3600,
                                                               (int(call.get('CALL_DURATION')) % 3600) // 60,
                                                               int(call.get('CALL_DURATION')) % 60)
                    user.DateCreate = call.get('CALL_START_DATE')
                    user.CALL_FAILED_CODE = call.get('CALL_FAILED_CODE')
                    user.CALL_TYPE = call.get('CALL_TYPE')
                    user.COMMENT = call.get('COMMENT')
                    user.save()
                else:
                    callControl.objects.create(
                        ID_CALL=call.get('ID'),
                        bitrix_staff_id_id=user_id,
                        PHONE_NUMBER=call.get('PHONE_NUMBER'),
                        DURATION='{:02}:{:02}:{:02}'.format(int(call.get('CALL_DURATION')) // 3600,
                                                            (int(call.get('CALL_DURATION')) % 3600) // 60,
                                                            int(call.get('CALL_DURATION')) % 60),
                        DateCreate=call.get('CALL_START_DATE'),
                        CALL_FAILED_CODE=call.get('CALL_FAILED_CODE'),
                        CALL_TYPE=call.get('CALL_TYPE'),
                        COMMENT=call.get('COMMENT')
                    )
            except CustomUser.DoesNotExist:
                pass

        '''Рабочее время'''
        emp_values = [{k: v if k != 'UF_DEPARTMENT' else ', '.join(map(str, v)) for k, v in d.items() if
                       k in ['ID', 'NAME', 'LAST_NAME', 'EMAIL', 'LAST_LOGIN', 'WORK_POSITION', 'UF_DEPARTMENT']} for d
                      in webhook.get_all('user.get')]
        user_id = [emp_values[i].get('ID') for i in range(len(emp_values))]
        data_time = [{'ID': id, **result} for id, result in
                     zip(user_id, [webhook.get_all('timeman.status', params={'USER_ID': int(id)}) for id in user_id])]

        for time in data_time:
            user_id = time.get('ID')
            print(user_id)
            try:
                user = TimeControl.objects.filter(bitrix_staff_id_id=user_id, START_TIME=time.get('TIME_START'))

                if user.exists():
                    user = user.first()
                    user.DURATION = time.get('DURATION')
                    user.TIME_LEAKS = time.get('TIME_LEAKS')
                    user.STATUS = time.get('STATUS')
                    user.START_TIME = time.get('TIME_START')
                    user.END_TIME = time.get('TIME_FINISH')
                    user.save()
                else:
                    TimeControl.objects.create(
                        bitrix_staff_id_id=user_id,
                        DURATION=time.get('DURATION'),
                        TIME_LEAKS=time.get('TIME_LEAKS'),
                        STATUS=time.get('STATUS'),
                        START_TIME=time.get('TIME_START'),
                        END_TIME=time.get('TIME_FINISH')
                    )
            except CustomUser.DoesNotExist:
                pass

        '''Сотрудники'''
        emp_values = [{k: v if k != 'UF_DEPARTMENT' else ', '.join(map(str, v)) for k, v in d.items() if
                       k in ['ID', 'NAME', 'LAST_NAME', 'EMAIL', 'LAST_LOGIN', 'WORK_POSITION', 'UF_DEPARTMENT']} for d
                      in webhook.get_all('user.get')]

        emp_values = [{**{k: v for k, v in case.items() if k != 'UF_DEPARTMENT'},
                       'UF_DEPARTMENT': {department['ID']: department['NAME'] for department in
                                         [{k: v for k, v in d.items() if k in ['ID', 'NAME']} for d in
                                          webhook.get_all('department.get')]}.get(case['UF_DEPARTMENT'], None)} for case
                      in emp_values]

        for data in emp_values:
            user_id = data.get('ID')
            try:
                user = CustomUser.objects.filter(bitrix_staff_id=user_id)

                if data.get('WORK_POSITION') == "Менеджер":
                    user_type = 1
                elif data.get('WORK_POSITION') == "Администратор":
                    user_type = 1
                else:
                    user_type = 2

                if user.exists():
                    user = user.first()
                    user.first_name = data.get('NAME')
                    user.email = data.get('EMAIL')
                    user.last_name = data.get('LAST_NAME')
                    user.last_login = data.get('LAST_LOGIN')
                    user.WORK_DEPARTMENT = data.get('UF_DEPARTMENT')
                    user.WORK_POSITION = data.get('WORK_POSITION')
                    user.user_type = user_type
                    user.save()
                else:
                    CustomUser.objects.create(
                        bitrix_staff_id=data.get('ID'),
                        first_name=data.get('NAME'),
                        email=data.get('EMAIL'),
                        last_name=data.get('LAST_NAME'),
                        last_login=data.get('LAST_LOGIN'),
                        WORK_DEPARTMENT=data.get('UF_DEPARTMENT'),
                        WORK_POSITION=data.get('WORK_POSITION'),
                        user_type=user_type
                    )
            except CustomUser.DoesNotExist:
                pass

        '''Задачи'''

        case_new_values = [{k: v for k, v in d.items() if
                            k in ['ID', 'RESPONSIBLE_ID', 'TITLE', 'DESCRIPTION', 'PRIORITY', 'REAL_STATUS', 'STATUS',
                                  'DEADLINE', 'TIME_ESTIMATE', 'CREATED_DATE', 'GROUP_ID']} for d in
                           webhook.get_all('task.item.list')]

        case_new_values = [{**{k: v for k, v in case.items() if k != 'GROUP_ID'},
                            'GROUP_ID': {department['ID']: department['NAME'] for department in
                                         [{k: v for k, v in d.items() if k in ['ID', 'NAME']} for d in
                                          webhook.get_all('sonet_group.get')]}.get(case['GROUP_ID'], None)} for case in
                           case_new_values]

        for case in case_new_values:
            task_id = case.get('ID')
            responsible_id = case.get('RESPONSIBLE_ID')

            try:
                custom_user = CustomUser.objects.get(bitrix_staff_id=responsible_id)
                DEADLINE = case.get('DEADLINE') if case.get('DEADLINE') != "" else None
                CREATED_DATE = case.get('CREATED_DATE') if case.get('CREATED_DATE') != "" else None
                tasks = TaskControl.objects.filter(ID_TASK=task_id)

                if tasks.exists():
                    task = tasks.first()
                    task.TITLE = case.get('TITLE')
                    task.DESCRIPTION = case.get('DESCRIPTION')
                    task.PRIORITY = case.get('PRIORITY')
                    task.STATUS = case.get('REAL_STATUS')
                    task.SUBSTATUS = case.get('STATUS')
                    task.DEADLINE = DEADLINE
                    task.TIME_ESTIMATE = case.get('TIME_ESTIMATE')
                    task.CREATED_DATE = CREATED_DATE
                    task.GROUP_PROJECTS = case.get('GROUP_ID')
                    task.bitrix_staff_id = custom_user
                    task.save()
                else:
                    TaskControl.objects.create(
                        ID_TASK=task_id,
                        TITLE=case.get('TITLE'),
                        DESCRIPTION=case.get('DESCRIPTION'),
                        PRIORITY=case.get('PRIORITY'),
                        STATUS=case.get('REAL_STATUS'),
                        SUBSTATUS=case.get('STATUS'),
                        DEADLINE=DEADLINE,
                        TIME_ESTIMATE=case.get('TIME_ESTIMATE'),
                        CREATED_DATE=CREATED_DATE,
                        GROUP_PROJECTS=case.get('GROUP_ID'),
                        bitrix_staff_id=custom_user
                    )

            except CustomUser.DoesNotExist:
                pass

    context = {
        'call_count': call_count,
        'task_count': task_count,
        'monthly_calls': monthly_calls,
        'monthly_task': monthly_task,
        'time_sum': time_sum,
        'monthly_calls_e': monthly_calls_e,
        'monthly_task_e': monthly_task_e
    }
    return render(request, 'Staff/home.html', context)


def NOTIFICATION(request):
    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id
        notification = Staff_Notification.objects.filter(staff_id=staff_id)
        context = {
            'notification': notification,
        }
        return render(request, 'Staff/staff_notification.html', context)


def STATUSNOTIFICATION(request, status):
    notification = Staff_Notification.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect('staff_notification')
