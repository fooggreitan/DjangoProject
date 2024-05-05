from django.conf import settings
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import CustomUser, Staff, Case, Task, TimeControl, Staff_Notification, Attendance_Report, Deal, Bitrix24
from django.contrib import messages
import google.generativeai as genai
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView
from app.models import Customer
from openai import ChatCompletion
import openai
from fast_bitrix24 import Bitrix
from datetime import datetime
import os


@login_required(login_url='/')
def HOME(request):
    staff_count = CustomUser.objects.filter(user_type='2').count()
    call_count = callControl.objects.all().count()
    task_count = TaskControl.objects.all().count()
    report_count = Attendance_Report.objects.all().count()

    from django.db.models.functions import ExtractMonth
    from django.db.models import Count, IntegerField, Sum

    monthly_calls = {}
    monthly_task = {}
    monthly_task_e = {}
    monthly_calls_e = {}

    calls = callControl.objects.filter(DateCreate__year=datetime.now().year)
    task = TaskControl.objects.filter(CREATED_DATE__year=datetime.now().year)
    months_of_interest = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

    for month_name in months_of_interest:
        month_number = datetime.strptime(month_name, "%B").month

        calls_less_30 = calls.filter(DURATION__lt='30', DateCreate__month=month_number).count()
        calls_more_5 = calls.filter(DURATION__gt='300', DateCreate__month=month_number).count()
        calls_normal = calls.filter(DURATION__lt='300', DURATION__gt='30', DateCreate__month=month_number).count()
        successful_calls = calls.filter(CALL_FAILED_CODE='200', DateCreate__month=month_number).count()

        completed_count = task.filter(STATUS='5', CREATED_DATE__month=month_number).count()
        overdue_task = task.filter(SUBSTATUS='-1', CREATED_DATE__month=month_number).count()
        needs_rework_count = task.filter(STATUS='7', CREATED_DATE__month=month_number).count()

        monthly_task[month_name] = {
            'needs_rework_count': needs_rework_count,
        }
        monthly_calls_e[month_name] = {
            'successful_calls': successful_calls,
        }
        monthly_task_e[month_name] = {
            'overdue_task': overdue_task,
            'completed_count': completed_count
        }
        monthly_calls[month_name] = {
            'total_calls_less_30': calls_less_30,
            'total_calls_more_5': calls_more_5,
            'total_calls_normal': calls_normal,
        }

    users = CustomUser.objects.filter(user_type=2)

    from datetime import timedelta

    analyzing_event = {' '.join((user.first_name, user.last_name)): {
        "call": callControl.objects.exclude(DURATION__isnull=True).filter(bitrix_staff_id=user, DateCreate__month=datetime.now().month, DateCreate__week=datetime.now().isocalendar().week).values() or [],
        "task": TaskControl.objects.exclude(id__isnull=True).filter(bitrix_staff_id=user, CREATED_DATE__month=datetime.now().month, CREATED_DATE__week=datetime.now().isocalendar().week).values() or [],
        "time": TimeControl.objects.exclude(id__isnull=True).filter(bitrix_staff_id=user, START_TIME__month=datetime.now().month, START_TIME__week=datetime.now().isocalendar().week).values() or [],
        "emp": CustomUser.objects.exclude(id__isnull=True).filter(bitrix_staff_id=user, date_joined__month=datetime.now().month, date_joined__week=datetime.now().isocalendar().week).values() or []
    } for user in users}

    analyzing_event = {user: data for user, data in analyzing_event.items() if any(data.values())}

    analyzing = {' '.join((user.first_name, user.last_name)): {
        "call": callControl.objects.filter(DURATION__lt='300', DURATION__gt='30', bitrix_staff_id=user,
                                           DateCreate__year=datetime.now().year).count(),
        "task": TaskControl.objects.filter(bitrix_staff_id=user, CREATED_DATE__year=datetime.now().year,
                                           STATUS='5').count(),
        "time": (TimeControl.objects.filter(bitrix_staff_id=user, START_TIME__year=datetime.now().year).values(
            'DURATION').aggregate(total_duration=Sum('DURATION'))['total_duration'] or timedelta(
            seconds=0)).total_seconds()
    } for user in users}

    sorted_analyzing = sorted(analyzing.items(), key=lambda x: (x[1]['call'], x[1]['task'], x[1]['time']), reverse=True)[:3]

    # sorted_analyzing_event = sorted(analyzing_event.items(), key=lambda x: (x[1]['call'], x[1]['task'], x[1]['time'], x[1]['emp']),
    #                           reverse=True)[:5]

    if Bitrix24.objects.get(name_webhook='one').webhook == '':
        redirect('hod_home')
    else:
        webhook = Bitrix(Bitrix24.objects.get(name_webhook='one').webhook)
        # webhook = Bitrix("https://b24-3kb71v.bitrix24.ru/rest/1/pkh1p9s7i4ylt49r/")

        '''Звонки'''

        call_values = [{k: v for k, v in d.items() if k in [
            'ID',
            'PORTAL_USER_ID',
            'CALL_TYPE',
            'PHONE_NUMBER',
            'CALL_DURATION',
            'CALL_START_DATE',
            'CALL_FAILED_CODE',
            'COMMENT'
        ]} for d in webhook.get_all('voximplant.statistic.get')]

        for call in call_values:
            user_id = call.get('PORTAL_USER_ID')
            print(user_id)
            try:
                user = callControl.objects.filter(ID_CALL=call.get('ID'))

                if user.exists():
                    user = user.first()
                    user.PHONE_NUMBER = call.get('PHONE_NUMBER')
                    user.DURATION = '{:02}:{:02}:{:02}'.format(int(call.get('CALL_DURATION')) // 3600, (int(call.get('CALL_DURATION')) % 3600) // 60, int(call.get('CALL_DURATION')) % 60)
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
                        DURATION = '{:02}:{:02}:{:02}'.format(int(call.get('CALL_DURATION')) // 3600, (int(call.get('CALL_DURATION')) % 3600) // 60, int(call.get('CALL_DURATION')) % 60),
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

        '''Сделки'''

        # res = [{k: v for k, v in d.items() if
        #         k in ['TITLE', 'DATE_CREATE', 'DATE_MODIFY', 'OPENED', 'TYPE_ID', 'ASSIGNED_BY_ID', 'CLOSEDATE']} for d
        #        in webhook.get_all('crm.deal.list')]
        #
        # for i in range(len(res)):
        #     assigned_by_id = res[i].get('ASSIGNED_BY_ID')
        #     try:
        #         custom_user = CustomUser.objects.get(bitrix_staff_id=assigned_by_id)
        #         # Пытаемся получить сделку из базы данных по критериям
        #         deal, created = Deal.objects.get_or_create(
        #             title=res[i].get('TITLE'),
        #             CLOSEDATE=res[i].get('CLOSEDATE'),
        #             Status=res[i].get('OPENED'),
        #             DATE_MODIFY=res[i].get('DATE_MODIFY'),
        #             TYPE_ID=res[i].get('TYPE_ID'),
        #             D ATE_CREATE=res[i].get('DATE_CREATE'),
        #             bitrix_staff_id=custom_user
        #         )
        #         if not created:
        #             # Если сделка уже существует, обновляем поля
        #             deal.CLOSEDATE = res[i].get('CLOSEDATE')
        #             deal.Status = res[i].get('OPENED')
        #             deal.DATE_MODIFY = res[i].get('DATE_MODIFY')
        #             deal.TYPE_ID = res[i].get('TYPE_ID')
        #             deal.DATE_CREATE = res[i].get('DATE_CREATE')
        #             deal.save()
        #     except CustomUser.DoesNotExist:
        #         # Если пользователь с таким bitrix_staff_id не найден, можно добавить соответствующую обработку ошибки или пропустить эту запись
        #         pass

        '''Дела'''

        # case_new_values = [{k: v for k, v in d.items() if
        #                     k in ['RESPONSIBLE_ID', 'DESCRIPTION', 'CREATED', 'LAST_UPDATED', 'COMPLETED', 'START_TIME',
        #                           'END_TIME', 'DEADLINE']} for d in webhook.get_all('crm.activity.list')]
        # for i in range(len(case_new_values)):
        #     responsible_id = case_new_values[i].get('RESPONSIBLE_ID')
        #     try:
        #         custom_user = CustomUser.objects.get(bitrix_staff_id=responsible_id)
        #         # Если пользователь найден, создаем или обновляем запись Case
        #         case, created = Case.objects.get_or_create(
        #             DESCRIPTION=case_new_values[i].get('DESCRIPTION'),
        #             CREATED=case_new_values[i].get('CREATED'),
        #             LAST_UPDATED=case_new_values[i].get('LAST_UPDATED'),
        #             COMPLETED=case_new_values[i].get('COMPLETED'),
        #             START_TIME=None,
        #             END_TIME=None,
        #             DEADLINE=case_new_values[i].get('DEADLINE'),
        #             bitrix_staff_id=custom_user
        #         )
        #         if not created:
        #             # Обновляем поля, если запись уже существует
        #             case.DESCRIPTION = case_new_values[i].get('DESCRIPTION')
        #             case.CREATED = case_new_values[i].get('CREATED')
        #             case.LAST_UPDATED = case_new_values[i].get('LAST_UPDATED')
        #             case.COMPLETED = case_new_values[i].get('COMPLETED')
        #             case.DEADLINE = case_new_values[i].get('DEADLINE')
        #             case.save()
        #     except CustomUser.DoesNotExist:
        #         # Если пользователь с таким bitrix_staff_id не найден, можно добавить соответствующую обработку ошибки или пропустить эту запись
        #         pass

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

                # Попытка получить задачи по ID_TASK
                tasks = TaskControl.objects.filter(ID_TASK=task_id)

                if tasks.exists():
                    # Обновление атрибутов первой найденной задачи
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
                    # Создание новой задачи
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
                # Если пользователь с таким bitrix_staff_id не найден, можно добавить соответствующую обработку ошибки или пропустить эту запись
                pass

    staff_male = Staff.objects.filter(gender='Male').count()
    staff_female = Staff.objects.filter(gender='Female').count()

    prompt = "Cделай краткое резюме по последним изменениям: {}".format(analyzing_event)

    import g4f
    from g4f.Provider import (
        FreeGpt,
        FreeChatgpt,
        AItianhu,
        Aichat,
        Bard,
        Bing,
        ChatBase,
        ChatgptAi,
        OpenaiChat,
        Vercel,
        You,
        Yqcloud,
        HuggingChat,
        OpenAssistant,
    )

    g4f.debug.logging = True  # enable logging
    g4f.check_version = False  # Disable automatic version checking

    g4f_request = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
        provider=g4f.Provider.FreeGpt
    )

    print(g4f_request)
    response = g4f_request

    context = {
        'staff_count': staff_count,
        'staff_male': staff_male,
        'staff_female': staff_female,
        'call_count': call_count,
        'task_count': task_count,
        'report_count': report_count,
        'monthly_calls': monthly_calls,
        'monthly_task': monthly_task,
        'sorted_analyzing': sorted_analyzing,
        'response': response,
        'monthly_calls_e': monthly_calls_e,
        'monthly_task_e': monthly_task_e
        # 'sorted_analyzing_event': sorted_analyzing_event
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
                profile_pic=profile_pic,
                first_name=first_name,
                last_name=last_name,
                email=email,
                user_type=2,
                username=username
            )
            user.set_password(password)
            user.save()

            staff = Staff(
                admin=user,
                address=address,
                gender=gender,
            )
            staff.save()
            messages.success(request, user.first_name + " " + user.last_name + "Персонал создан!")
            return redirect('add_staff')
    return render(request, 'Hod/add_staff.html')


@login_required(login_url='/')
def VIEW_STAFF(request):
    if Bitrix24.objects.get(name_webhook='one').webhook == '':
        redirect('hod_home')
    else:
        webhook = Bitrix(Bitrix24.objects.get(name_webhook='one').webhook)

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

                if data.get('WORK_POSITION') == "Менеджер" or data.get('WORK_POSITION') == "Руководитель":
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

    staff = CustomUser.objects.filter(user_type=2)
    context = {
        'staff': staff,
    }
    return render(request, 'Hod/view_staff.html', context)


@login_required(login_url='/')
def EDIT_STAFF(request, id):
    staff = Staff.objects.get(id=id)
    context = {
        'staff': staff,
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


@login_required(login_url='/')
def STAFF_SEND_NOTIFICATION(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all().order_by('-id')[0:5]
    context = {
        'staff': staff,
        'see_notification': see_notification
    }
    return render(request, 'Hod/staff_send_notification.html', context)


@login_required(login_url='/')
def STAFF_SAVE_NOTIFICATION(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin=staff_id)
        notification = Staff_Notification(
            staff_id=staff,
            message=message,
        )
        notification.save()
        messages.success(request, 'Всё отправлено')
    return redirect('staff_send_notification')


@login_required(login_url='/')
def ABOUT_PROFILE(request):
    staff = Staff.objects.all()
    context = {
        'staff': staff,
    }
    return render(request, 'Hod/about_profile.html', context)


@login_required(login_url='/')
def VIEW_STAFF_TASK(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all().order_by('-id')
    context = {
        'staff': staff,
        'see_notification': see_notification
    }
    return render(request, 'Staff/view_task.html', context)


@login_required(login_url='/')
def ADD_REPORT(request):
    report = Attendance_Report.objects.all()
    content = {
        "content": report,
    }
    return render(request, 'Hod/add_report.html', content)


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from app.models import Customer

# class AppListView(ListView):
#     model = Customer
#     template_name = 'Hod/add_report.html'

from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import render_to_string
import os


# class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
#         # getting the template
#         data = Attendance_Report.objects.get(id = 5)
#         open('templates/temp.html', "w").write(render_to_string('report/pdf2.html', {'data': data}))
#         pdf = app_render_pdf_view('temp.html')
#         # rendering the template
#         return HttpResponse(pdf, content_type='application/pdf')

def DELETEREPORT(request, id):
    delete_report = Attendance_Report.objects.get(id=id)
    delete_report.delete()
    messages.success(request, "Успешно удален!")
    return redirect('add_report')


import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

# def link_callback(uri, rel):
#     """
#     Convert HTML URIs to absolute system paths so xhtml2pdf can access those
#     resources
#     """
#     result = finders.find(uri)
#     if result:
#         if not isinstance(result, (list, tuple)):
#             result = [result]
#         result = list(os.path.realpath(path) for path in result)
#         path = result[0]
#     else:
#         sUrl = settings.STATIC_URL
#         sRoot = settings.STATIC_ROOT
#         mUrl = settings.MEDIA_URL
#         mRoot = settings.MEDIA_ROOT
#
#         if uri.startswith(mUrl):
#             path = os.path.join(mRoot, uri.replace(mUrl, ""))
#         elif uri.startswith(sUrl):
#             path = os.path.join(sRoot, uri.replace(sUrl, ""))
#         else:
#             return uri
#
#     print(
#         "path: " + path,
#         "result: " + result
#     )
#
#     # make sure that file exists
#     if not os.path.isfile(path):
#         raise RuntimeError(
#             'media URI must start with %s or %s' % (sUrl, mUrl)
#         )
#     return path

import pdfkit
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.loader import get_template


# def app_render_pdf_view(request):
#     data = Attendance_Report.objects.get(id=id)
#     context = {'pdf': data}
#
#     html = render_to_string('pdf2.html', context)
#     pdf = pdfkit.from_string(html, False)
#     filename = "sample_pdf.pdf"
#
#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="' + filename + '"'
#     return response

def app_render_pdf_view(request, id):
    # data = Attendance_Report.objects.get(id=id)
    data = Attendance_Report.objects.filter(id=id).values('progress', 'Errors', 'practices_improving_your',
                                                          'general_comment', 'possible_risks', 'created_at',
                                                          'name_report')

    json_dict = {
        "progress": '',
        'error': '',
        'recommendations': '',
        'comment': '',
        'risks': ''
    }

    for data_report in data:
        json_dict['progress'] = data_report['progress']
        json_dict['error'] = data_report['Errors']
        json_dict['recommendations'] = data_report['practices_improving_your']
        json_dict['comment'] = data_report['general_comment']
        json_dict['risks'] = data_report['possible_risks']

    # import re
    #
    # description = [section.strip() for section in re.sub('', '',
    #                                                      Attendance_Report.objects.filter(id=id).values('description')[
    #                                                          0].get('description')).replace('\n', " ").split('  ') if
    #                section.strip()]
    # dict = [line.replace('**', '') for line in description]

    # successes = []
    # errors = []
    # recommendations = []
    # comments = []
    # risks = []

    # for i in range(len(dict)):
    #     if dict[i] == 'Успехи:':
    #         successes.append(dict[i + 1].replace('. ', '.\n'))
    #         json_dict['progress'] = '\n'.join(successes)
    #     elif dict[i] == 'Ошибки:':
    #         errors.append(dict[i + 1].replace('. ', '.\n'))
    #         json_dict['error'] = '\n'.join(errors)
    #     elif dict[i] == 'Рекомендации по улучшению работы:':
    #         recommendations.append(dict[i + 1].replace('. ', '.\n'))
    #         json_dict['recommendations'] = '\n'.join(recommendations)
    #     elif dict[i] == 'Общий комментарий:':
    #         comments.append(dict[i + 1].replace('. ', '.\n'))
    #         json_dict['comment'] = '\n'.join(comments)
    #     elif dict[i] == 'Возможные риски:':
    #         risks.append(dict[i + 1].replace('. ', '.\n'))
    #         json_dict['risks'] = '\n'.join(risks)
    #
    print(json_dict)

    # for i in range(3):
    #     res = Attendance_Report.objects.filter(id=id).values('description')[0].get('description').replace('*', '').replace('\n', ' ').replace(':', '').split("[")[1:][i].split(']')
    #     dict[res[0]] = res[1]

    username = CustomUser.objects.filter(
        bitrix_staff_id__in=Attendance_Report.objects.filter(staff_id=43).values_list(
            'staff_id', flat=True
        )).values(
        'first_name', 'last_name', 'WORK_DEPARTMENT', 'WORK_POSITION'
    )

    print("username: {0}".format(username))

    template = get_template('pdf2.html')
    content = {
        'pdf': data,
        "username": username,
        "dict": json_dict
    }

    html = template.render(content)
    pdf = pdfkit.from_string(html, False, options={
        'encoding': "UTF-8",
        "enable-local-file-access": ""
    })
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    return response


# def app_render_pdf_view(request, id):
#     data = Attendance_Report.objects.get(id=id)
#     template_path = 'pdf2.html'
#     context = {'pdf': data}
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="report.pdf"'
#     template = get_template(template_path)
#     html = template.render(context)
#     pisa_status = pisa.CreatePDF(
#         html.encode('UTF-8'), dest=response, encoding='UTF-8', link_callback=link_callback)
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response


# def chatbot_view(request):
#     print(request)
#     if request.method == 'POST':
#         user_input = request.POST.get('user_input')
#         print(user_input)
#         content = {
#             'user_input': user_input
#         }
#         return render(request, 'Hod/add_report.html', content)
#     else:
#         request.session.clear()
#         return render(request, 'Hod/add_report.html', {'conversation': "Не получилось"})

from django.http import JsonResponse


# def chatbot(request):
#     if request.method == "POST":
#         # message = request.POST.get('message')
#         response = "привет"
# #         content = {
# #             "response": response
# #         }
#         return render(request, 'Hod/add_report.html', content)
#     return render(request, 'Hod/add_report.html')

# @login_required(login_url='/')
# def app_render_pdf_view(request, *args, **kwargs):
#     report_pdf = kwargs.get('pk')
#     app_report = get_object_or_404(Customer, pk=report_pdf)
#     template_path = 'report/pdf2.html'  # шаблон
#     context = {'app_report': app_report}  # передеча в шаблон
#     # Create a Django response object, and specify content_type as pdf
#     response = HttpResponse(content_type='application/pdf')
#     # if download:
#     # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     # if display:
#     response['Content-Disposition'] = 'filename="report.pdf"'
#     # find the template and render it.
#     template = get_template(template_path)
#     html = template.render(context)
#
#     # create a pdf
#     pisa_status = pisa.CreatePDF(
#         html, dest=response)
#     # if error then show some funny view
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response
def VIEW_DEAL(request):
    deal = Deal.objects.all()
    context = {
        "deal": deal
    }
    return render(request, "Hod/view_deal.html", context)


def VIEW_CASE(request):
    case = Case.objects.all()
    context = {
        "case": case
    }
    return render(request, "Hod/view_case.html", context)


def BITRIX(request):
    webhook = Bitrix24.objects.filter(name_webhook='one')
    context = {
        "webhook": webhook
    }
    return render(request, "Hod/webhook_bitrix24.html", context)


def NEW_WEBHOOK(request):
    if Bitrix24.objects.get(name_webhook='one').webhook == request.POST.get("WEBHOOK"):
        messages.warning(request, "Вы ничего не изменили")
    else:
        Bitrix24.objects.filter(name_webhook='one').update(webhook=request.POST.get("WEBHOOK"))
        messages.success(request, "Вы успешно изменили webhook")
    return redirect('add_bitrix24')


# def UPDATE_DATE(request):
#     webhook = Bitrix(Bitrix24.objects.get(id=1).webhook)
#     res = [{k: v for k, v in d.items() if
#             k in ['RESPONSIBLE_ID', 'DESCRIPTION', 'CREATED', 'LAST_UPDATED', 'COMPLETED', 'START_TIME', 'END_TIME',
#                   'DEADLINE']} for d in webhook.get_all('crm.activity.list')]
#     for i in range(len(res)):
#         user = Case(DESCRIPTION=res[i].get('DESCRIPTION'), CREATED=res[i].get('CREATED'),
#                     LAST_UPDATED=res[i].get('LAST_UPDATED'), COMPLETED=res[i].get('COMPLETED'),
#                     START_TIME=res[i].get('START_TIME'), END_TIME=res[i].get('END_TIME'),
#                     DEADLINE=res[i].get('DEADLINE'),
#                     bitrix_staff_id=CustomUser.objects.get(bitrix_staff_id=res[i].get('RESPONSIBLE_ID')))
#         user.save()
#     return redirect('hod_home')

from app.models import TaskControl
from django.utils import timezone


def TASKCONTROL(request):
    global deferred_count, in_progress_count, needs_rework_count, overdue_count, task, waitingTask, newTask, presumably_completed, task_almost_overdue, unreviewed_task, overdue_task, presumably_completed_t, task_almost_overdue_t, unreviewed_task_t, overdue_task_t, newTask_t, waitingTask_t, completed_count_t, needs_rework_count_t, in_progress_count_t, deferred_count_t, completed_count

    if Bitrix24.objects.get(name_webhook='one').webhook == '':
        redirect('hod_home')
    else:
        webhook = Bitrix(Bitrix24.objects.get(name_webhook='one').webhook)

        '''Задачи'''

        task_new = [{k: v for k, v in d.items() if k in [
            'ID', 'RESPONSIBLE_ID',
            'TITLE',
            'DESCRIPTION',
            'PRIORITY',
            'REAL_STATUS',
            'STATUS',
            'DEADLINE',
            'TIME_ESTIMATE',
            'CREATED_DATE',
            'GROUP_ID']} for d in  webhook.get_all('task.item.list')]

        task_new_values = [{**{k: v for k, v in case.items() if k != 'GROUP_ID'},'GROUP_ID': {department['ID']: department['NAME'] for department in
                                         [{k: v for k, v in d.items() if k in ['ID', 'NAME']} for d in
                                          webhook.get_all('sonet_group.get')]}.get(case['GROUP_ID'], None)} for case in
                           task_new]

        for case in task_new_values:
            task_id = case.get('ID')
            responsible_id = case.get('RESPONSIBLE_ID')

            try:
                custom_user = CustomUser.objects.get(bitrix_staff_id=responsible_id)
                DEADLINE = case.get('DEADLINE') if case.get('DEADLINE') != "" else None
                CREATED_DATE = case.get('CREATED_DATE') if case.get('CREATED_DATE') != "" else None

                # Попытка получить задачи по ID_TASK
                tasks = TaskControl.objects.filter(ID_TASK=task_id)

                if tasks.exists():
                    # Обновление атрибутов первой найденной задачи
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
                    # Создание новой задачи
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
                # Если пользователь с таким bitrix_staff_id не найден, можно добавить соответствующую обработку ошибки или пропустить эту запись
                pass

    select_type = ''

    if request.method == 'POST':
        select_type = request.POST.get('select_type_period')

    if request.user.user_type == '1':
        users = CustomUser.objects.filter(user_type=2)
    else:
        users = CustomUser.objects.filter(bitrix_staff_id=request.user.bitrix_staff_id, user_type=2)

    tasks_per_user = {}

    for user in users:
        if select_type == 'month':
            task = TaskControl.objects.filter(CREATED_DATE__month=datetime.now().month,
                                              CREATED_DATE__year=datetime.now().year)
            user_tasks = TaskControl.objects.filter(bitrix_staff_id=user,
                                                    CREATED_DATE__month=datetime.now().month,
                                                    CREATED_DATE__year=datetime.now().year)
        elif select_type == 'week':
            task = TaskControl.objects.filter(CREATED_DATE__week=datetime.now().isocalendar().week,
                                              CREATED_DATE__year=datetime.now().year)
            user_tasks = TaskControl.objects.filter(bitrix_staff_id=user,
                                                    CREATED_DATE__week=datetime.now().isocalendar().week,
                                                    CREATED_DATE__year=datetime.now().year)
        elif select_type == 'day':
            task = TaskControl.objects.filter(CREATED_DATE__day=datetime.now().day,
                                              CREATED_DATE__month=datetime.now().month,
                                              CREATED_DATE__year=datetime.now().year)
            user_tasks = TaskControl.objects.filter(bitrix_staff_id=user,
                                                    CREATED_DATE__day=datetime.now().day,
                                                    CREATED_DATE__month=datetime.now().month,
                                                    CREATED_DATE__year=datetime.now().year)
        else:
            task = TaskControl.objects.all()
            user_tasks = TaskControl.objects.filter(bitrix_staff_id=user)

        deferred_count = user_tasks.filter(STATUS='6').count()
        in_progress_count = user_tasks.filter(STATUS='3').count()
        needs_rework_count = user_tasks.filter(STATUS='7').count()
        completed_count = user_tasks.filter(STATUS='5').count()
        newTask = user_tasks.filter(STATUS='1').count()
        waitingTask = user_tasks.filter(STATUS='2').count()
        presumably_completed = user_tasks.filter(STATUS='4').count()
        unreviewed_task = user_tasks.filter(SUBSTATUS='-2').count()
        overdue_task = user_tasks.filter(SUBSTATUS='-1').count()
        task_almost_overdue = user_tasks.filter(SUBSTATUS='-3').count()

        tasks_per_user[user] = {
            "deferred_count": deferred_count,
            "in_progress_count": in_progress_count,
            "needs_rework_count": needs_rework_count,
            "completed_count": completed_count,
            "waitingTask": waitingTask,
            "newTask": newTask,
            "presumably_completed": presumably_completed,
            "task_almost_overdue": task_almost_overdue,
            "unreviewed_task": unreviewed_task,
            "overdue_task": overdue_task,
            "user_type": user.user_type
        }

    if request.user.user_type == '1':
        deferred_count = task.filter(STATUS='6').count()
        in_progress_count = task.filter(STATUS='3').count()
        needs_rework_count = task.filter(STATUS='7').count()
        completed_count = task.filter(STATUS='5').count()

        newTask = task.filter(STATUS='1').count()
        waitingTask = task.filter(STATUS='2').count()
        presumably_completed = task.filter(STATUS='4').count()

        task_almost_overdue = task.filter(SUBSTATUS='-3').count()
        unreviewed_task = task.filter(SUBSTATUS='-2').count()
        overdue_task = task.filter(SUBSTATUS='-1').count()

    context = {
        "tasks_per_user": tasks_per_user,
        "task": task,
        "deferred_count": deferred_count,
        "in_progress_count": in_progress_count,
        "needs_rework_count": needs_rework_count,
        "completed_count": completed_count,
        "waitingTask": waitingTask,
        "newTask": newTask,
        "presumably_completed": presumably_completed,
        "task_almost_overdue": task_almost_overdue,
        "unreviewed_task": unreviewed_task,
        "overdue_task": overdue_task,
        "current_user": request.user,
    }
    return render(request, "Hod/taskControl.html", context)

def TIMECONTROL(request):

    if Bitrix24.objects.get(name_webhook='one').webhook == '':
        redirect('hod_home')
    else:
        webhook = Bitrix(Bitrix24.objects.get(name_webhook='one').webhook)

        emp_values = [{k: v if k != 'UF_DEPARTMENT' else ', '.join(map(str, v)) for k, v in d.items() if k in [
            'ID',
            'NAME',
            'LAST_NAME',
            'EMAIL',
            'LAST_LOGIN',
            'WORK_POSITION',
            'UF_DEPARTMENT'
        ]} for d in webhook.get_all('user.get')]

        user_id = [
            emp_values[i].get('ID') for i in range(len(emp_values))
        ]
        data_time = [
            {'ID': id, **result} for id, result in zip(
                user_id, [webhook.get_all(
                    'timeman.status',
                    params={'USER_ID': int(id)}
                ) for id in user_id]
            )
        ]

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

    select_type = ''

    if request.method == 'POST' :
        select_type = request.POST.get('select_type_period')

    if select_type == 'month':
        time = TimeControl.objects.filter(START_TIME__month=datetime.now().month,
                                          START_TIME__year=datetime.now().year)
    elif select_type == 'week':
        time = TimeControl.objects.filter(START_TIME__week=datetime.now().isocalendar().week,
                                          START_TIME__year=datetime.now().year)
    elif select_type == 'day':
        time = TimeControl.objects.filter(START_TIME__day=datetime.now().day,
                                          START_TIME__month=datetime.now().month,
                                          START_TIME__year=datetime.now().year)
    else:
        time = TimeControl.objects.all()

    context = {
        "time": time,
    }
    return render(request, "Hod/time_control.html", context)


from app.models import callControl

def CALLCONTROL(request):

    global call, number_calls_less_30, number_calls_more_5, total_Incoming_calls, total_outgoing_calls, total_missed_calls, busy_calls, rejected_calls

    if Bitrix24.objects.get(name_webhook='one').webhook == '':
        redirect('hod_home')
    else:
        webhook = Bitrix(Bitrix24.objects.get(name_webhook='one').webhook)

        '''Звонки'''

        call_values = [{k: v for k, v in d.items() if k in [
            'ID',
            'PORTAL_USER_ID',
            'CALL_TYPE',
            'PHONE_NUMBER',
            'CALL_DURATION',
            'CALL_START_DATE',
            'CALL_FAILED_CODE',
        ]} for d in webhook.get_all('voximplant.statistic.get')]

        for call in call_values:
            user_id = call.get('PORTAL_USER_ID')
            print(user_id)
            try:
                user = callControl.objects.filter(ID_CALL=call.get('ID'))

                if user.exists():
                    user = user.first()
                    user.PHONE_NUMBER = call.get('PHONE_NUMBER')
                    user.DURATION = '{:02}:{:02}:{:02}'.format(
                        int(call.get('CALL_DURATION')) // 3600, (int(call.get('CALL_DURATION')) % 3600) // 60, int(call.get('CALL_DURATION')) % 60)
                    user.DateCreate = call.get('CALL_START_DATE')
                    user.CALL_FAILED_CODE = call.get('CALL_FAILED_CODE')
                    user.CALL_TYPE = call.get('CALL_TYPE')
                    user.save()
                else:
                    callControl.objects.create(
                        ID_CALL=call.get('ID'),
                        bitrix_staff_id_id=user_id,
                        PHONE_NUMBER=call.get('PHONE_NUMBER'),
                        DURATION = '{:02}:{:02}:{:02}'.format(
                            int(call.get('CALL_DURATION')) // 3600, (int(call.get('CALL_DURATION')) % 3600) // 60, int(call.get('CALL_DURATION')) % 60),
                        DateCreate=call.get('CALL_START_DATE'),
                        CALL_FAILED_CODE=call.get('CALL_FAILED_CODE'),
                        CALL_TYPE=call.get('CALL_TYPE'),
                    )
            except CustomUser.DoesNotExist:
                pass

    select_report_type = ''

    if request.method == 'POST':
        select_report_type = request.POST.get('select_type_period')

    users = CustomUser.objects.filter(user_type=2, WORK_DEPARTMENT='Отдел поддержки клиентов')
    call_per_user = {}

    for user in users:
        if select_report_type == 'month':
            call = callControl.objects.filter(DateCreate__month=datetime.now().month,
                                              DateCreate__year=datetime.now().year,
                                              )
            user_call = callControl.objects.filter(bitrix_staff_id=user,
                                                   DateCreate__month=datetime.now().month,
                                                   DateCreate__year=datetime.now().year
                                                   )
        elif select_report_type == 'week':
            call = callControl.objects.filter(DateCreate__week=datetime.now().isocalendar().week,
                                              DateCreate__year=datetime.now().year)
            user_call = callControl.objects.filter(bitrix_staff_id=user,
                                                   DateCreate__week=datetime.now().isocalendar().week,
                                                   DateCreate__year=datetime.now().year
                                                   )
        elif select_report_type == 'day':
            call = callControl.objects.filter(DateCreate__day=datetime.now().day,
                                              DateCreate__month=datetime.now().month,
                                              DateCreate__year=datetime.now().year)
            user_call = callControl.objects.filter(bitrix_staff_id=user,
                                                   DateCreate__day=datetime.now().day,
                                                   DateCreate__month=datetime.now().month,
                                                   DateCreate__year=datetime.now().year
                                                   )
        else:
            call = callControl.objects.all()
            user_call = callControl.objects.filter(bitrix_staff_id=user)

        number_calls_less_30 = user_call.filter(DURATION__lt='30').count(),
        number_calls_more_5 = user_call.filter(DURATION__gt='300').count(),
        total_Incoming_calls = user_call.filter(CALL_TYPE='1').count(),
        total_outgoing_calls = user_call.filter(CALL_TYPE='2').count(),
        total_missed_calls = user_call.filter(CALL_FAILED_CODE='304').count(),
        successful_calls = user_call.filter(CALL_FAILED_CODE='200').count(),
        rejected_calls = user_call.filter(CALL_FAILED_CODE='603').count(),
        busy_calls = user_call.filter(CALL_FAILED_CODE='486').count(),

        call_per_user[user] = {
            "number_calls_less_30": number_calls_less_30[0],
            "number_calls_more_5": number_calls_more_5[0],
            "total_Incoming_calls": total_Incoming_calls[0],
            "total_outgoing_calls": total_outgoing_calls[0],
            "total_missed_calls": total_missed_calls[0],
            "rejected_calls": rejected_calls[0],
            "busy_calls": busy_calls[0],
            "user_type": user.user_type[0],
        }

        if request.user.user_type == '1':
            number_calls_less_30 = call.filter(DURATION__lt='30').count(),
            number_calls_more_5 = call.filter(DURATION__gt='300').count(),
            total_Incoming_calls = call.filter(CALL_TYPE='1').count(),
            total_outgoing_calls = call.filter(CALL_TYPE='2').count(),
            total_missed_calls = call.filter(CALL_FAILED_CODE='304').count(),
            rejected_calls = call.filter(CALL_FAILED_CODE='603').count(),
            busy_calls = call.filter(CALL_FAILED_CODE='486').count(),

    print(call_per_user)
    context = {
        "call_per_user": call_per_user,
        "number_calls_less_30": number_calls_less_30[0],
        "number_calls_more_5": number_calls_more_5[0],
        "total_Incoming_calls": total_Incoming_calls[0],
        "total_outgoing_calls": total_outgoing_calls[0],
        "total_missed_calls": total_missed_calls[0],
        "rejected_calls": rejected_calls[0],
        "busy_calls": busy_calls[0],
        "current_user": request.user,  # Добавляем текущего пользователя в контекст
        "call": call,

    }
    return render(request, "Hod/call_view.html", context)


def chatbot_view(request, *args, **kwargs):
    global staff_id, first_name, last_name, customer, prompt

    if request.method == 'POST':
        select_report_type = request.POST.get('select_type_report')
        select_type_staff = request.POST.get('select_type_staff')
        select_departament = request.POST.get('select_departament')

        select_type_staff_split = select_type_staff.split()
        first_name = select_type_staff_split[0]
        last_name = select_type_staff_split[1]

        if select_departament != 'Отдел не выбран' and select_type_staff != "Сотрудник не выбран":
            customer = CustomUser.objects.filter(
                user_type=2,
                WORK_DEPARTMENT=select_departament,
                first_name=first_name,
                last_name=last_name).values('first_name', 'last_name', 'WORK_POSITION', 'WORK_DEPARTMENT')
            users = CustomUser.objects.filter(
                user_type=2,
                WORK_DEPARTMENT=select_departament)
        elif select_departament == 'Отдел не выбран' and select_type_staff != "Сотрудник не выбран":
            customer = CustomUser.objects.filter(
                user_type=2,
                first_name=first_name,
                last_name=last_name).values('first_name', 'last_name', 'WORK_POSITION', 'WORK_DEPARTMENT')
            users = CustomUser.objects.filter(user_type=2, first_name=first_name, last_name=last_name)
        elif select_departament != 'Отдел не выбран' and select_type_staff == "Сотрудник не выбран":
            customer = CustomUser.objects.filter(
                user_type=2,
                WORK_DEPARTMENT=select_departament).values('first_name', 'last_name', 'WORK_POSITION',
                                                           'WORK_DEPARTMENT')
            users = CustomUser.objects.filter(user_type=2, WORK_DEPARTMENT=select_departament)
        else:
            customer = CustomUser.objects.filter(
                user_type=2).values('first_name', 'last_name', 'WORK_POSITION', 'WORK_DEPARTMENT')
            users = CustomUser.objects.filter(user_type=2)

        print(customer)
        print(select_report_type)
        print(select_type_staff)

        # genai.configure(api_key=os.getenv('KEY_MODEL_AI'))
        #
        # generation_config = {
        #     "temperature": 0.9,
        #     "top_p": 1,
        #     "top_k": 1,
        #     "max_output_tokens": 2048,
        # }
        #
        # safety_settings = [
        #     {
        #         "category": "HARM_CATEGORY_HARASSMENT",
        #         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        #     },
        #     {
        #         "category": "HARM_CATEGORY_HATE_SPEECH",
        #         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        #     },
        #     {
        #         "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        #         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        #     },
        #     {
        #         "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        #         "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        #     },
        # ]
        #
        # model = genai.GenerativeModel(
        #     model_name="gemini-1.0-pro",
        #     generation_config=generation_config,
        #     safety_settings=safety_settings
        # )

        from datetime import datetime
        import pandas as pd

        anlazing_task = ''
        anlazing_time = ''
        anlazing_call = ''
        anlazing_deal = ''
        anlazing_case = ''

        if select_report_type != 'Отчёт не выбран':
            if select_report_type == 'Отчет о проделанной работе за месяц':
                anlazing_call = {' '.join((user.first_name, user.last_name)): {
                    "calls_less_that_30_seconds_count": callControl.objects.filter(bitrix_staff_id=user,
                                                                                   DURATION__lt='30',
                                                                                   DateCreate__year=datetime.now().year,
                                                                                   DateCreate__month=datetime.now().month).count(),
                    "calls_more_that_5_minutes_count": callControl.objects.filter(bitrix_staff_id=user,
                                                                                  DURATION__gt='300',
                                                                                  DateCreate__year=datetime.now().year,
                                                                                  DateCreate__month=datetime.now().month).count(),
                    "total_Incoming_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='1',
                                                                             DateCreate__year=datetime.now().year,
                                                                             DateCreate__month=datetime.now().month).count(),
                    "total_outgoing_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                             DateCreate__year=datetime.now().year,
                                                                             DateCreate__month=datetime.now().month).count(),
                    "total_missed_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='304',
                                                                           DateCreate__year=datetime.now().year,
                                                                           DateCreate__month=datetime.now().month).count(),

                    "rejected_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='603',
                                                                       DateCreate__year=datetime.now().year,
                                                                       DateCreate__week=datetime.now().month).count(),
                    "busy_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='486',
                                                                   DateCreate__year=datetime.now().year,
                                                                   DateCreate__week=datetime.now().month).count(),
                }
                    for user in users
                }

                anlazing_task = {' '.join((user.first_name, user.last_name)): {
                    "tasks_deferred_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='6',
                                                                       CREATED_DATE__year=datetime.now().year,
                                                                       CREATED_DATE__month=datetime.now().month).count(),
                    "tasks_in_progress_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='3',
                                                                          CREATED_DATE__year=datetime.now().year,
                                                                          CREATED_DATE__month=datetime.now().month).count(),
                    "tasks_needs_rework_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='7',
                                                                           CREATED_DATE__year=datetime.now().year,
                                                                           CREATED_DATE__month=datetime.now().month).count(),
                    "tasks_overdue_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='5',
                                                                      CREATED_DATE__year=datetime.now().year,
                                                                      CREATED_DATE__month=datetime.now().month).count(),

                    "tasks_newTask_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='1',
                                                                      CREATED_DATE__year=datetime.now().year,
                                                                      CREATED_DATE__month=datetime.now().month).count(),
                    "tasks_waitingTask_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='2',
                                                                          CREATED_DATE__year=datetime.now().year,
                                                                          CREATED_DATE__month=datetime.now().month).count(),
                    "tasks_presumably_completed_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='4',
                                                                                   CREATED_DATE__year=datetime.now().year,
                                                                                   CREATED_DATE__month=datetime.now().month).count(),
                } for user in users}

                anlazing_time = {' '.join((user.first_name, user.last_name)): {
                    "time": TimeControl.objects.filter(bitrix_staff_id=user, START_TIME__year=datetime.now().year,
                                                       START_TIME__month=datetime.now().month).values('TIME_LEAKS',
                                                                                                      'DURATION')
                } for user in users}

            elif select_report_type == 'Отчет о проделанной работе за день':
                anlazing_call = {' '.join((user.first_name, user.last_name)): {
                    "calls_less_that_30_seconds_count": callControl.objects.filter(bitrix_staff_id=user,
                                                                                   DURATION__lt='30',
                                                                                   DateCreate__year=datetime.now().year,
                                                                                   DateCreate__month=datetime.now().month,
                                                                                   DateCreate__day=datetime.now().day).count(),
                    "calls_more_that_5_minutes_count": callControl.objects.filter(bitrix_staff_id=user,
                                                                                  DURATION__gt='300',
                                                                                  DateCreate__year=datetime.now().year,
                                                                                  DateCreate__month=datetime.now().month,
                                                                                  DateCreate__day=datetime.now().day).count(),
                    "total_Incoming_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='1',
                                                                             DateCreate__year=datetime.now().year,
                                                                             DateCreate__month=datetime.now().month,
                                                                             DateCreate__day=datetime.now().day).count(),
                    "total_outgoing_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                             DateCreate__year=datetime.now().year,
                                                                             DateCreate__month=datetime.now().month,
                                                                             DateCreate__day=datetime.now().day).count(),
                    "total_missed_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='304',
                                                                           DateCreate__year=datetime.now().year,
                                                                           DateCreate__month=datetime.now().month,
                                                                           DateCreate__day=datetime.now().day).count(),

                    "rejected_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='603',
                                                                       DateCreate__year=datetime.now().year,
                                                                       DateCreate__month=datetime.now().month,
                                                                       DateCreate__week=datetime.now().day).count(),
                    "busy_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='486',
                                                                   DateCreate__year=datetime.now().year,
                                                                   DateCreate__month=datetime.now().month,
                                                                   DateCreate__week=datetime.now().day).count(),
                }
                    for user in users
                }

                anlazing_task = {' '.join((user.first_name, user.last_name)): {
                    "tasks_deferred_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='6',
                                                                       CREATED_DATE__year=datetime.now().year,
                                                                       CREATED_DATE__month=datetime.now().month,
                                                                       CREATED_DATE__day=datetime.now().day).count(),
                    "tasks_in_progress_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='3',
                                                                          CREATED_DATE__year=datetime.now().year,
                                                                          CREATED_DATE__month=datetime.now().month,
                                                                          CREATED_DATE__day=datetime.now().day).count(),
                    "tasks_needs_rework_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='7',
                                                                           CREATED_DATE__year=datetime.now().year,
                                                                           CREATED_DATE__month=datetime.now().month,
                                                                           CREATED_DATE__day=datetime.now().day).count(),
                    "tasks_overdue_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='5',
                                                                      CREATED_DATE__year=datetime.now().year,
                                                                      CREATED_DATE__month=datetime.now().month,
                                                                      CREATED_DATE__day=datetime.now().day).count(),

                    "tasks_newTask_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='1',
                                                                      CREATED_DATE__year=datetime.now().year,
                                                                      CREATED_DATE__month=datetime.now().month,
                                                                      CREATED_DATE__day=datetime.now().day).count(),
                    "tasks_waitingTask_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='2',
                                                                          CREATED_DATE__year=datetime.now().year,
                                                                          CREATED_DATE__month=datetime.now().month,
                                                                          CREATED_DATE__day=datetime.now().day).count(),
                    "tasks_presumably_completed_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='4',
                                                                                   CREATED_DATE__year=datetime.now().year,
                                                                                   CREATED_DATE__month=datetime.now().month,
                                                                                   CREATED_DATE__day=datetime.now().day).count(),
                } for user in users}

                anlazing_time = {' '.join((user.first_name, user.last_name)): {
                    "time": TimeControl.objects.filter(bitrix_staff_id=user, START_TIME__year=datetime.now().year,
                                                       START_TIME__month=datetime.now().month,
                                                       START_TIME__day=datetime.now().day).values('TIME_LEAKS',
                                                                                                  'DURATION')
                } for user in users}

            elif select_report_type == 'Отчет о проделанной работе за неделю':
                anlazing_call = {' '.join((user.first_name, user.last_name)): {
                    "calls_less_that_30_seconds_count": callControl.objects.filter(bitrix_staff_id=user,
                                                                                   DURATION__lt='30',
                                                                                   DateCreate__year=datetime.now().year,
                                                                                   DateCreate__week=datetime.now().isocalendar().week).count(),
                    "calls_more_that_5_minutes_count": callControl.objects.filter(bitrix_staff_id=user,
                                                                                  DURATION__gt='300',
                                                                                  DateCreate__year=datetime.now().year,
                                                                                  DateCreate__week=datetime.now().isocalendar().week).count(),
                    "total_Incoming_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='1',
                                                                             DateCreate__year=datetime.now().year,
                                                                             DateCreate__week=datetime.now().isocalendar().week).count(),
                    "total_outgoing_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                             DateCreate__year=datetime.now().year,
                                                                             DateCreate__week=datetime.now().isocalendar().week).count(),
                    "total_missed_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='304',
                                                                           DateCreate__year=datetime.now().year,
                                                                           DateCreate__week=datetime.now().isocalendar().week).count(),

                    "rejected_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='603',
                                                                       DateCreate__year=datetime.now().year,
                                                                       DateCreate__week=datetime.now().isocalendar().week).count(),
                    "busy_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='486',
                                                                   DateCreate__year=datetime.now().year,
                                                                   DateCreate__week=datetime.now().isocalendar().week).count(),
                } for user in users}
                anlazing_task = {' '.join((user.first_name, user.last_name)): {
                    "tasks_deferred_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='6',
                                                                       CREATED_DATE__year=datetime.now().year,
                                                                       CREATED_DATE__week=datetime.now().isocalendar().week).count(),
                    "tasks_in_progress_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='3',
                                                                          CREATED_DATE__year=datetime.now().year,
                                                                          CREATED_DATE__week=datetime.now().isocalendar().week).count(),
                    "tasks_needs_rework_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='7',
                                                                           CREATED_DATE__year=datetime.now().year,
                                                                           CREATED_DATE__week=datetime.now().isocalendar().week).count(),
                    "tasks_overdue_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='5',
                                                                      CREATED_DATE__year=datetime.now().year,
                                                                      CREATED_DATE__week=datetime.now().isocalendar().week).count(),

                    "tasks_newTask_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='1',
                                                                      CREATED_DATE__year=datetime.now().year,
                                                                      CREATED_DATE__week=datetime.now().isocalendar().week).count(),
                    "tasks_waitingTask_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='2',
                                                                          CREATED_DATE__year=datetime.now().year,
                                                                          CREATED_DATE__week=datetime.now().isocalendar().week).count(),
                    "tasks_presumably_completed_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='4',
                                                                                   CREATED_DATE__year=datetime.now().year,
                                                                                   CREATED_DATE__week=datetime.now().isocalendar().week).count(),
                } for user in users}

                anlazing_time = {' '.join((user.first_name, user.last_name)): {
                    "time": TimeControl.objects.filter(bitrix_staff_id=user, START_TIME__year=datetime.now().year,
                                                       START_TIME__week=datetime.now().isocalendar().week).values(
                        'TIME_LEAKS', 'DURATION')
                } for user in users}

            print(anlazing_task)
            print(anlazing_time)
            print(anlazing_call)

            anlazing_task = pd.DataFrame(anlazing_task)
            anlazing_time = pd.DataFrame(anlazing_time)
            anlazing_call = pd.DataFrame(anlazing_call)

            prompt = ''
            staff_id = ''

            if select_departament == "Отдел не выбран":
                if select_type_staff == "Сотрудник не выбран":
                    prompt = """
                    \nВступай в роли бота, который пишет {0} от третьего лица (от лица компании "Эркью") по сотрудникам:{1}.
                    \nВ отчёте должна содержаться детальная информация **об анализе качества и эффективности работы cотрудников** учитывая все параметры:
                    \nанализ задач сотрудников:{2}, анализ рабочего времени сотрудников:{3}.
                    \nДля **нарушения качества работы сотрудников** принимай параметр **количества задач отправленные на доработку больше 2 раз**
                    \nДля **определния трудовой дисциплины сотрудников** организации принимай параметр: **количество опозданий** и **время рабочее и перерыва**.
                    \nОтчёт должен содержать заголовки:
                    \nУспехи:детальная информация о преимуществах работы сотрудников {1} за {0}.
                    \nОшибки:детальная информация о недостатках работы сотрудников {1} за {0}.
                    \nОбщий комментарий:выводы по работе сотрудников {1}.
                    \nВозможные риски:укажи возможные риски эффективности работы сотрудников организации на основе исторических данных:анализ задач сотрудников:{2},
                    \nанализ рабочего времени сотрудников:{3}.
                    \nРекомендации по улучшению работы:статьи, книги, документация для прочтения сотрудниками организации {1}.
                    \nСледуй всем требованиям формирования отчёта контроля качества и эффективности работы сотрудников организации и 
                    \nпредоставляй **точные числовые значения работы сотруднков**.
                    \nИнформация должна быть подробно описана в заголовках: Успехи:, Ошибки:, Общий комментарий:, Рекомендации по улучшению работы:, Возможные риски:.
                    \nФормат вывода заголовков отчёта:
                    \nУспехи:[сотрудник_1, cотрудник_2 ... сотрудник_N],
                    \nОшибки:[сотрудник_1, cотрудник_2 ... сотрудник_N],
                    \nРекомендации по улучшению работы:[сотрудник_1, cотрудник_2 ... сотрудник_N],
                    \nОбщий комментарий:[сотрудник_1, cотрудник_2 ... сотрудник_N],
                    \nВозможные риски:[риск_1, риск_2 ... риск_N].\n\n\n
                    """.format(
                        select_report_type, customer, anlazing_task, anlazing_time
                    )
                else:
                    prompt = """
                    \nВступай в роли бота, который пишет {0} от третьего лица (от лица компании "Эркью") по сотруднику {1} с должностью {4} в {5}.
                    \nВ отчёте должна содержаться детальная информация ***об анализе качества и эффективности работы cотрудника** учитывая все параметры:
                    \nанализ задач сотрудника:{2}, анализ рабочего времени сотрудника:{3}.
                    \nДля **нарушения качества работы сотрудника** принимай параметр **количества задач отправленные на доработку больше 2 раз**
                    \nДля **определния трудовой дисциплины сотрудника** организации принимай параметр: **количество опозданий** и **время рабочее и перерыва**.
                    \nОтчёт должен содержать заголовки:
                    \nУспехи: детальная информация о преимуществах сотрудника {1} за {0}.
                    \nОшибки: детальная информация о недостатках работы сотрудника {1} за {0}.
                    \nОбщий комментарий: выводы по работе сотрудника {1}.
                    \nРекомендации по улучшению работы:статьи, книги, документация для прочтения сотрудником организации {1}.
                    \nВозможные риски: укажи возможные риски эффективности работы сотрудника организации на основе исторических данных: анализ задач сотрудника:{2},
                    \nанализ рабочего времени сотрудника:{3}.
                    \nСледуй всем требованиям формирования отчёта контроля качества и эффективности работы сотрудников организации и 
                    \nпредоставляй **точные числовые значения работы сотруднка**.
                    \nИнформация должна быть подробно описана в заголовках: Успехи:, Ошибки:, Общий комментарий:, Рекомендации по улучшению работы:, Возможные риски:.
                    \nФормат вывода заголовков отчёта:
                    \nУспехи:[Успех_1, Успех_2 ... Успех_N],
                    \nОшибки:[Ошибки_1, Ошибки_2 ... Ошибки_N],
                    \nРекомендации по улучшению работы:[Рекомендация_1, Рекомендация_2 ... Рекомендация_N],
                    \nОбщий комментарий:[Общая информация].
                    \nВозможные риски:[риск_1, риск_2 ... риск_N].\n\n\n
                    """.format(select_report_type, select_type_staff, anlazing_task, anlazing_time,
                               customer.first().get('WORK_POSITION'), customer.first().get('WORK_DEPARTMENT')
                               )

            elif select_departament == "Отдел поддержки клиентов":
                if select_type_staff == "Сотрудник не выбран":
                    prompt = """
                    \nВступай в роли бота, который пишет {0} от третьего лица (от лица компании "Эркью") по сотрудникам отдела поддержки клиентов:{1}.
                    \nВ отчёте должна содержаться детальная информация **об анализе качества и эффективности работы cотрудников** отдела поддержки клиентов учитывая все параметры:
                    \nанализ задач сотрудников:{2}, анализ рабочего времени сотрудника:{3}, анализ звонков сотрудников:{4}.
                    \nДля **нарушения качества работы сотрудников** отдела поддержки клиентов принимай параметры: 
                    \n**количества задач отправленные на доработку больше 2 раз**, **время звонка меньше 30 секунд и больше 5 минут**.
                    \nДля **определния трудовой дисциплины сотрудников** организации отдела поддержки клиентов принимай параметр: **количество опозданий** и **время рабочее и перерыва**.
                    \nОтчёт должен содержать заголовки:
                    \nУспехи:детальная информация о преимуществах сотрудников {1} за {0}.
                    \nОшибки:детальная информация о недостатках работы сотрудников {1} за {0}.
                    \nОбщий комментарий:выводы по работе сотрудников {1}.
                    \nВозможные риски:укажи возможные риски эффективности работы сотрудников организации на основе исторических данных:анализ задач сотрудников:{2},
                    \nанализ рабочего времени сотрудников:{3}, анализ звонков сотрудников:{4}.
                    \nРекомендации по улучшению работы:статьи, книги, документация для прочтения сотрудниками организации {1}.
                    \nСледуй всем требованиям формирования отчёта контроля качества и эффективности работы сотрудников организации и 
                    \nпредоставляй **точные числовые значения работы сотруднков**.
                    \nИнформация должна быть подробно описана в заголовках: Успехи:, Ошибки:, Общий комментарий:, Рекомендации по улучшению работы:, Возможные риски:.
                    \nФормат вывода заголовков отчёта:
                    \nУспехи:[сотрудник_1, cотрудник_2 ... сотрудник_N],
                    \nОшибки:[сотрудник_1, cотрудник_2 ... сотрудник_N],
                    \nРекомендации по улучшению работы:[сотрудник_1, cотрудник_2 ... сотрудник_N],
                    \nОбщий комментарий:[сотрудник_1, cотрудник_2 ... сотрудник_N],
                    \nВозможные риски:[риск_1, риск_2 ... риск_N].\n\n\n
                    """.format(
                        select_report_type, customer, anlazing_task, anlazing_time, anlazing_call
                    )
                else:
                    prompt = """
                    \nВступай в роли бота, который пишет {0} от третьего лица (от лица компании "Эркью") по сотруднику отдела поддержки клиентов:{1}.
                    \nВ отчёте должна содержаться детальная информация **об анализе качества и эффективности работы cотрудника** отдела поддержки клиентов учитывая все параметры:
                    \nанализ задач сотрудника:{2}, анализ рабочего времени сотрудника:{3}, анализ звонков сотрудника:{4}.
                    \nДля **нарушения качества работы сотрудника** отдела поддержки клиентов принимай параметры: 
                    \n**количества задач отправленные на доработку больше 2 раз**, **время звонка меньше 30 секунд и больше 5 минут**.
                    \nДля **определния трудовой дисциплины сотрудника** организации отдела поддержки клиентов принимай параметр: **количество опозданий** и **время рабочее и перерыва**.
                    \nОтчёт должен содержать заголовки:
                    \nУспехи:детальная информация о преимуществах сотрудника {1} за {0}.
                    \nОшибки:детальная информация о недостатках работы сотрудника {1} за {0}.
                    \nОбщий комментарий:выводы по работе сотрудника {1}.
                    \nВозможные риски:укажи возможные риски эффективности работы сотрудника организации на основе исторических данных:анализ задач сотрудника:{2},
                    \nанализ рабочего времени сотрудника:{3}, анализ звонков сотрудника:{4}.
                    \nРекомендации по улучшению работы сотрудника:статьи, книги, документация для прочтения сотрудником организации {1}.
                    \nСледуй всем требованиям формирования отчёта контроля качества и эффективности работы сотрудника организации и 
                    \nпредоставляй **точные числовые значения работы сотруднка**.
                    \nИнформация должна быть подробно описана в заголовках: Успехи:, Ошибки:, Общий комментарий:, Рекомендации по улучшению работы:, Возможные риски:.
                    \nФормат вывода заголовков отчёта:
                    \nУспехи:[Успех_1, Успех_2 ... Успех_N],
                    \nОшибки:[Ошибки_1, Ошибки_2 ... Ошибки_N],
                    \nРекомендации по улучшению работы:[Рекомендация_1, Рекомендация_2 ... Рекомендация_N],
                    \nОбщий комментарий:[Общая информация].
                    \nВозможные риски:[риск_1, риск_2 ... риск_N].\n\n\n
                    """.format(
                        select_report_type, select_type_staff, anlazing_task, anlazing_time, anlazing_call,
                        customer.first().get('WORK_POSITION'), customer.first().get('WORK_DEPARTMENT')
                    )

            if select_type_staff != "Сотрудник не выбран":
                staff_add = CustomUser.objects.filter(
                    first_name=first_name,
                    last_name=last_name,
                    user_type=2
                ).values_list("bitrix_staff_id", flat=True)[0]
                staff_id = str(staff_add)
            else:
                staff_id = 'Все сотрудники'

            import g4f
            from g4f.Provider import (
                FreeGpt,
                FreeChatgpt,
                AItianhu,
                Aichat,
                Bard,
                Bing,
                ChatBase,
                ChatgptAi,
                OpenaiChat,
                Vercel,
                You,
                Yqcloud,
                HuggingChat,
                OpenAssistant,
            )

            g4f.debug.logging = True  # enable logging
            g4f.check_version = False  # Disable automatic version checking

            g4f_request = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt},
                ],
                provider=g4f.Provider.FreeGpt
            )

            print(g4f_request)
            description = g4f_request
            staff = CustomUser.objects.filter(user_type=2)

            import re
            descriptions = re.sub('', '', description).replace('\n', " ").split('  ')
            # descriptions = [section.strip() for section in re.sub('', '', description).replace('\n', " ").split('  ') if section.strip()]
            dict = [line.replace('**', '') for line in descriptions]

            print(dict)

            successes = []
            errors = []
            recommendations = []
            comments = []
            risks = []

            json_dict = {
                "progress": '',
                'error': '',
                'recommendations': '',
                'comment': '',
                'risks': ''
            }

            for i in range(len(dict)):
                if dict[i] == 'Успехи:':
                    successes.append(dict[i + 1].replace('. ', '.\n'))
                    json_dict['progress'] = '\n'.join(successes)
                elif dict[i] == 'Ошибки:':
                    errors.append(dict[i + 1].replace('. ', '.\n'))
                    json_dict['error'] = '\n'.join(errors)
                elif dict[i] == 'Рекомендации по улучшению работы:':
                    recommendations.append(dict[i + 1].replace('. ', '.\n'))
                    json_dict['recommendations'] = '\n'.join(recommendations)
                elif dict[i] == 'Общий комментарий:':
                    comments.append(dict[i + 1].replace('. ', '.\n'))
                    json_dict['comment'] = '\n'.join(comments)
                elif dict[i] == 'Возможные риски:':
                    risks.append(dict[i + 1].replace('. ', '.\n'))
                    json_dict['risks'] = '\n'.join(risks)

            print(json_dict)

            context = {
                "response": description,
                "description": description,
                "staff_id": staff_id,
                "select_type_staff": select_type_staff,
                "select_report_type": select_report_type,
                "staff": staff,

                "progress": json_dict['progress'],
                "errors": json_dict['error'],
                "recommendations": json_dict['recommendations'],
                "comment": json_dict['comment'],
                "risks": json_dict['risks'],
            }

            # messages.success(request, "Вы успешно создали отчёт!")
            return render(request, 'Hod/report_create.html', context)
        else:
            messages.error(request, "Вы некорректно указали фильтр")
            return redirect('add_report')
    else:
        request.session.clear()
        return render(request, 'Hod/add_report.html', {'conversation': "Не получилось"})


def create_new_report(request, *args, **kwargs):
    if request.method == 'POST':

        staff_id = request.POST.get('staff_id')
        select_type_staff = request.POST.get('select_type_staff')
        select_report_type = request.POST.get('select_report_type')
        description = request.POST.get('description')

        if select_type_staff == "Сотрудник не выбран":
            add_new_report = Attendance_Report(
                name_report=select_report_type,
                description=description,
                progress=request.POST.get('ex1'),
                Errors=request.POST.get('ex2'),
                practices_improving_your=request.POST.get('ex3'),
                general_comment=request.POST.get('ex4'),
                possible_risks=request.POST.get('ex5'),
            )
        else:
            add_new_report = Attendance_Report(
                name_report=select_report_type,
                description=description,
                progress=request.POST.get('ex1'),
                Errors=request.POST.get('ex2'),
                practices_improving_your=request.POST.get('ex3'),
                general_comment=request.POST.get('ex4'),
                possible_risks=request.POST.get('ex5'),
                staff_id=staff_id
            )

        add_new_report.save()

        messages.success(request, "Вы успешно создали отчёт!")
        return redirect('add_report')
    else:
        messages.error(request, "Вы некорректно указали фильтр")
        return redirect('add_report')


def REPORTCREATE(request):
    report = Attendance_Report.objects.all()
    staff = CustomUser.objects.filter(user_type=2)
    content = {
        "content": report,
        "staff": staff,
    }
    return render(request, "Hod/report_create.html", content)
