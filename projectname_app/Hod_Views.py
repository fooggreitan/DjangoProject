from django.conf import settings
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

    if Bitrix24.objects.get(name_webhook='one').webhook == '':
        redirect('hod_home')
    else:
        webhook = Bitrix(Bitrix24.objects.get(name_webhook='one').webhook)
        # webhook = Bitrix("https://b24-buvcaf.bitrix24.ru/rest/1/3c1qfeilajoo8exh/")

        '''Сотрудники'''
        # emp_values = [{k: v if k != 'UF_DEPARTMENT' else ', '.join(map(str, v)) for k, v in d.items() if
        #                k in ['ID', 'NAME', 'LAST_NAME', 'EMAIL', 'LAST_LOGIN', 'WORK_POSITION', 'UF_DEPARTMENT']} for d
        #               in webhook.get_all('user.get')]
        #
        # emp_values = [{**{k: v for k, v in case.items() if k != 'UF_DEPARTMENT'},
        #                'UF_DEPARTMENT': {department['ID']: department['NAME'] for department in
        #                                  [{k: v for k, v in d.items() if k in ['ID', 'NAME']} for d in
        #                                   webhook.get_all('department.get')]}.get(case['UF_DEPARTMENT'], None)} for case in emp_values]
        #
        # for i in range(len(emp_values)):
        #     obj, created = CustomUser.objects.get_or_create(
        #         bitrix_staff_id=emp_values[i].get('ID'),
        #         first_name = emp_values[i].get('NAME'),
        #         email = emp_values[i].get('EMAIL'),
        #         last_name = emp_values[i].get('LAST_NAME'),
        #         last_login = emp_values[i].get('LAST_LOGIN'),
        #         WORK_DEPARTMENT = emp_values[i].get('UF_DEPARTMENT'),
        #         WORK_POSITION=emp_values[i].get('WORK_POSITION'),
        #     )
        #     if not created:
        #         obj.first_name = emp_values[i].get('NAME')
        #         obj.email = emp_values[i].get('EMAIL')
        #         obj.last_name = emp_values[i].get('LAST_NAME')
        #         obj.last_login = emp_values[i].get('LAST_LOGIN')
        #         obj.WORK_DEPARTMENT = emp_values[i].get('UF_DEPARTMENT'),
        #         obj.WORK_POSITION = emp_values[i].get('WORK_POSITION'),
        #         obj.save()

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
        #             DATE_CREATE=res[i].get('DATE_CREATE'),
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
                            k in ['RESPONSIBLE_ID', 'TITLE', 'DESCRIPTION', 'PRIORITY', 'REAL_STATUS', 'STATUS',
                                  'DEADLINE', 'TIME_ESTIMATE', 'CREATED_DATE', 'GROUP_ID']} for d in
                           webhook.get_all('task.item.list')]

        case_new_values = [{**{k: v for k, v in case.items() if k != 'GROUP_ID'},
                            'GROUP_ID': {department['ID']: department['NAME'] for department in
                                         [{k: v for k, v in d.items() if k in ['ID', 'NAME']} for d in
                                          webhook.get_all('sonet_group.get')]}.get(case['GROUP_ID'], None)} for case in
                           case_new_values]


        for i in range(len(case_new_values)):
            responsible_id = case_new_values[i].get('RESPONSIBLE_ID')
            try:
                custom_user = CustomUser.objects.get(bitrix_staff_id=responsible_id)

                DEADLINE = case_new_values[i].get('DEADLINE') if case_new_values[i].get('DEADLINE') != "" else None
                CREATED_DATE = case_new_values[i].get('CREATED_DATE') if case_new_values[i].get(
                    'CREATED_DATE') != "" else None

                task, created = TaskControl.objects.get_or_create(
                    TITLE=case_new_values[i].get('TITLE'),
                    DESCRIPTION=case_new_values[i].get('DESCRIPTION'),
                    PRIORITY=case_new_values[i].get('PRIORITY'),
                    STATUS=case_new_values[i].get('REAL_STATUS'),
                    SUBSTATUS= "-" + case_new_values[i].get('STATUS'),
                    DEADLINE=DEADLINE,
                    TIME_ESTIMATE=case_new_values[i].get('TIME_ESTIMATE'),
                    CREATED_DATE=CREATED_DATE,
                    GROUP_PROJECTS=case_new_values[i].get('GROUP_ID'),
                    bitrix_staff_id=custom_user
                )
                if not created:
                    task.TITLE = case_new_values[i].get('TITLE')
                    task.DESCRIPTION = case_new_values[i].get('DESCRIPTION')
                    task.PRIORITY = case_new_values[i].get('PRIORITY')
                    task.STATUS = case_new_values[i].get('REAL_STATUS')
                    task.SUBSTATUS = "-" + case_new_values[i].get('STATUS')
                    task.DEADLINE = DEADLINE
                    task.TIME_ESTIMATE = case_new_values[i].get('TIME_ESTIMATE')
                    task.CREATED_DATE = CREATED_DATE
                    task.GROUP_PROJECTS = case_new_values[i].get('GROUP_ID')

                    task.save()

            except CustomUser.DoesNotExist:
                # Если пользователь с таким bitrix_staff_id не найден, можно добавить соответствующую обработку ошибки или пропустить эту запись
                pass

    staff_male = Staff.objects.filter(gender='Male').count()
    staff_female = Staff.objects.filter(gender='Female').count()

    context = {
        'staff_count': staff_count,
        'staff_male': staff_male,
        'staff_female': staff_female,
        'call_count': call_count,
        'task_count': task_count,
        'report_count': report_count
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
    # print(request.method)
    #
    # if request.method == "POST":
    #     # message = request.POST.get('message')
    #     response = 'Привет'
    #     content = {
    #         "response": response
    #     }
    #     return render(request, 'Hod/add_report.html', content)

    report = Attendance_Report.objects.all()
    staff = Staff.objects.all()

    response = "f"

    content = {
        "content": report,
        "staff": staff,
        "response": response
    }
    print(content)
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

def DELETEPDF(request, id):
    delete_pdf = Attendance_Report.objects.get(id=id)
    delete_pdf.delete()
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
                                                          'general_comment', 'possible_risks')

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
        id__in=Attendance_Report.objects.filter(id=id).values_list(
            'staff_id', flat=True
        )).values(
        'first_name', 'last_name'
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

    select_report_type = ''

    if request.method == 'POST':
        select_report_type = request.POST.get('select_type_report')
        print(select_report_type)

    users = CustomUser.objects.filter(user_type=2)
    tasks_per_user = {}

    for user in users:
        if select_report_type == 'month':
            task = TaskControl.objects.filter(CREATED_DATE__month=datetime.now().month,
                                              CREATED_DATE__year=datetime.now().year)
            user_tasks = TaskControl.objects.filter(bitrix_staff_id=user,
                                                    CREATED_DATE__month=datetime.now().month,
                                                    CREATED_DATE__year=datetime.now().year
                                                    )
        elif select_report_type == 'week':
            task = TaskControl.objects.filter(CREATED_DATE__week=datetime.now().isocalendar().week,
                                              CREATED_DATE__year=datetime.now().year)
            user_tasks = TaskControl.objects.filter(bitrix_staff_id=user,
                                                    CREATED_DATE__week=datetime.now().isocalendar().week,
                                                    CREATED_DATE__year=datetime.now().year
                                                    )
        elif select_report_type == 'day':
            task = TaskControl.objects.filter(CREATED_DATE__day=datetime.now().day,
                                              CREATED_DATE__year=datetime.now().year)
            user_tasks = TaskControl.objects.filter(bitrix_staff_id=user,
                                                    CREATED_DATE__day=datetime.now().day,
                                                    CREATED_DATE__year=datetime.now().year
                                                    )
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

        task_almost_overdue = user_tasks.filter(SUBSTATUS='-3').count()
        unreviewed_task = user_tasks.filter(SUBSTATUS='-2').count()
        overdue_task = user_tasks.filter(SUBSTATUS='-1').count()

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
        "current_user": request.user  # Добавляем текущего пользователя в контекст
    }

    return render(request, "Hod/taskControl.html", context)


def TIMECONTROL(request):
    time = TimeControl.objects.all()
    context = {
        "time": time,
    }
    return render(request, "Hod/time_control.html", context)


from app.models import callControl


def CALLCONTROL(request):

    global call, number_calls_less_30, number_calls_more_5, total_Incoming_calls, total_outgoing_calls, total_missed_calls, busy_calls, rejected_calls

    select_report_type = ''

    if request.method == 'POST':
        select_report_type = request.POST.get('select_type_report')

    users = CustomUser.objects.filter(user_type=2)
    call_per_user = {}

    for user in users:
        if select_report_type == 'month':
            call = callControl.objects.filter(DateCreate__month=datetime.now().month,
                                              DateCreate__year=datetime.now().year)
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
                                              DateCreate__year=datetime.now().year)
            user_call = callControl.objects.filter(bitrix_staff_id=user,
                                                   DateCreate__day=datetime.now().day,
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
    global prompt
    print(request)
    # conversation = request.session.get('conversation', [])
    if request.method == 'POST':
        select_report_type = request.POST.get('select_type_report')
        select_type_staff = request.POST.get('select_type_staff')
        select_departament = request.POST.get('select_departament')

        select_type_staff_split = select_type_staff.split()

        first_name_parts = select_type_staff_split[0]
        last_name_parts = select_type_staff_split[1]

        first_name = first_name_parts.split()
        last_name = last_name_parts.split()

        # first_name, last_name = select_type_staff_split.split()

        # user_input = request.POST.get('textPostSelect')
        # print(user_input)

        if select_departament != 'Отдел не выбран' and select_type_staff != "Сотрудник не выбран":
            customer = CustomUser.objects.filter(user_type=2, WORK_DEPARTMENT=select_departament, first_name=first_name,
                                                 last_name=last_name).values('first_name', 'last_name', 'WORK_POSITION',
                                                                             'WORK_DEPARTMENT')
            users = CustomUser.objects.filter(user_type=2, WORK_DEPARTMENT=select_departament)
        elif select_departament == 'Отдел не выбран' and select_type_staff != "Сотрудник не выбран":
            customer = CustomUser.objects.filter(user_type=2, first_name=first_name, last_name=last_name).values(
                'first_name', 'last_name', 'WORK_POSITION', 'WORK_DEPARTMENT')
            users = CustomUser.objects.filter(user_type=2, first_name=first_name, last_name=last_name)
        elif select_departament != 'Отдел не выбран' and select_type_staff == "Сотрудник не выбран":
            customer = CustomUser.objects.filter(user_type=2, WORK_DEPARTMENT=select_departament).values(
                'first_name', 'last_name', 'WORK_POSITION', 'WORK_DEPARTMENT')
            users = CustomUser.objects.filter(user_type=2, WORK_DEPARTMENT=select_departament)
        else:
            customer = CustomUser.objects.filter(user_type=2).values('first_name', 'last_name', 'WORK_POSITION',
                                                                     'WORK_DEPARTMENT')
            users = CustomUser.objects.filter(user_type=2)

        # staff = CustomUser.objects.filter(
        #     id__in=Staff.objects.values_list('admin_id', flat=True)
        # ).values('first_name', 'last_name')
        #
        # for i in staff:
        #     customer += "{0} {1} \n".format(i['first_name'], i['last_name'])

        print(customer)
        print(select_report_type)
        print(select_type_staff)

        if select_report_type != 'Отчёт не выбран':

            genai.configure(api_key="AIzaSyDRK2DTmNY61tutvN2n_W51O0diOrr5ulU")

            generation_config = {
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }

            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
            ]

            model = genai.GenerativeModel(
                model_name="gemini-1.0-pro",
                generation_config=generation_config,
                safety_settings=safety_settings
            )

            '''ChatGTP'''
            # prompts = []

            # '''Начальный системный промт'''
            #
            # prompts.append({"role": "system", "content": """
            #     Ты являешься ботом который формирует отчёты от третьего лица (от лица компании Эркью)
            #     Ты должен следовать всем требованиям формирования отчётов для эффективности и контроля
            #     работы сотрудников организации. Вывод информации должен содержать заголовки [Успехи:], [Ошибки:], [Рекомендации по улучшению работы:], [Общий комментарий:].
            # """})
            #
            # '''Промт сотрудника за месяц'''
            #
            # if select_type_staff == "Сотрудник не выбран":
            #     prompts.append({"role": "user", "content": "Cделай {0} включая каждого сотрудников {1}".format(
            #         select_report_type,
            #         customer
            #     )})
            # else:
            #     prompts.append({"role": "user", "content": "Cделай {0} по сотруднику {1}".format(
            #         select_report_type,
            #         select_type_staff
            #     )})

            # response = openai.ChatCompletion.create(
            #     model="ft:gpt-3.5-turbo-0613:personal::7wZAALHG",
            #     messages=prompts,
            #     api_key="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",
            #     max_tokens=1200,
            #     temperature=0.2,
            #     top_p=1,
            #     frequency_penalty=0.5,
            #     presence_penalty=0.5
            # )

            '''' Создание отчёта'''

            anlazing_task = ''
            anlazing_time = ''
            anlazing_call = ''

            anlazing_deal = ''
            anlazing_case = ''

            from datetime import datetime
            import pandas as pd

            if select_report_type == 'Отчет о проделанной работе за месяц':
                anlazing_call = {' '.join((user.first_name, user.last_name)): {
                    "calls_less_that_30_seconds": callControl.objects.filter(bitrix_staff_id=user, DURATION__lt='30',
                                                                             DateCreate__year=datetime.now().year,
                                                                             DateCreate__month=datetime.now().month).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "calls_less_that_30_seconds_count": callControl.objects.filter(bitrix_staff_id=user,
                                                                                   DURATION__lt='30',
                                                                                   DateCreate__year=datetime.now().year,
                                                                                   DateCreate__month=datetime.now().month).count(),
                    "calls_more_that_5_minutes": callControl.objects.filter(bitrix_staff_id=user, DURATION__gt='300',
                                                                            DateCreate__year=datetime.now().year,
                                                                            DateCreate__month=datetime.now().month).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "calls_more_that_5_minutes_count": callControl.objects.filter(bitrix_staff_id=user,
                                                                                  DURATION__gt='300',
                                                                                  DateCreate__year=datetime.now().year,
                                                                                  DateCreate__month=datetime.now().month).count(),
                    "total_Incoming_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='1',
                                                                       DateCreate__year=datetime.now().year,
                                                                       DateCreate__month=datetime.now().month).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "total_Incoming_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='1',
                                                                             DateCreate__year=datetime.now().year,
                                                                             DateCreate__month=datetime.now().month).count(),
                    "total_outgoing_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                       DateCreate__year=datetime.now().year,
                                                                       DateCreate__month=datetime.now().month).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "total_outgoing_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                             DateCreate__year=datetime.now().year,
                                                                             DateCreate__month=datetime.now().month).count(),
                    "total_missed_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='304',
                                                                     DateCreate__year=datetime.now().year,
                                                                     DateCreate__month=datetime.now().month).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "total_missed_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='304',
                                                                           DateCreate__year=datetime.now().year,
                                                                           DateCreate__month=datetime.now().month).count(),
                    "rejected_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                 DateCreate__year=datetime.now().year,
                                                                 DateCreate__week=datetime.now().month).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "rejected_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                       DateCreate__year=datetime.now().year,
                                                                       DateCreate__week=datetime.now().month).count(),
                    "busy_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                             DateCreate__year=datetime.now().year,
                                                             DateCreate__week=datetime.now().month).values(
                        'PHONE_NUMBER',
                        'VOTE', 'COST',
                        'DateCreate'),
                    "busy_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                   DateCreate__year=datetime.now().year,
                                                                   DateCreate__week=datetime.now().month).count(),
                }
                    for user in users
                }

                anlazing_task = {' '.join((user.first_name, user.last_name)): {
                    "tasks_deferred": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='6',
                                                                 CREATED_DATE__year=datetime.now().year,
                                                                 CREATED_DATE__month=datetime.now().month).values(
                        'TITLE', 'DESCRIPTION', 'DEADLINE', 'TIME_ESTIMATE'),
                    "tasks_deferred_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='6',
                                                                       CREATED_DATE__year=datetime.now().year,
                                                                       CREATED_DATE__month=datetime.now().month).count(),
                    "tasks_in_progress": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='3',
                                                                    CREATED_DATE__year=datetime.now().year,
                                                                    CREATED_DATE__month=datetime.now().month).values(
                        'TITLE', 'DESCRIPTION', 'DEADLINE', 'TIME_ESTIMATE'),
                    "tasks_in_progress_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='3',
                                                                          CREATED_DATE__year=datetime.now().year,
                                                                          CREATED_DATE__month=datetime.now().month).count(),
                    "tasks_needs_rework": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='7',
                                                                     CREATED_DATE__year=datetime.now().year,
                                                                     CREATED_DATE__month=datetime.now().month).values(
                        'TITLE', 'DESCRIPTION', 'DEADLINE', 'TIME_ESTIMATE'),
                    "tasks_needs_rework_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='7',
                                                                           CREATED_DATE__year=datetime.now().year,
                                                                           CREATED_DATE__month=datetime.now().month).count(),
                    "tasks_overdue": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='5',
                                                                CREATED_DATE__year=datetime.now().year,
                                                                CREATED_DATE__month=datetime.now().month).values(
                        'TITLE', 'DESCRIPTION', 'DEADLINE', 'TIME_ESTIMATE'),
                    "tasks_overdue_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='5',
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
                    "calls_less_that_30_seconds": callControl.objects.filter(bitrix_staff_id=user, DURATION__lt='30',
                                                                             DateCreate__year=datetime.now().year,
                                                                             DateCreate__day=datetime.now().day).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "calls_less_that_30_seconds_count": callControl.objects.filter(bitrix_staff_id=user,
                                                                                   DURATION__lt='30',
                                                                                   DateCreate__year=datetime.now().year,
                                                                                   DateCreate__day=datetime.now().day).count(),
                    "calls_more_that_5_minutes": callControl.objects.filter(bitrix_staff_id=user, DURATION__gt='300',
                                                                            DateCreate__year=datetime.now().year,
                                                                            DateCreate__day=datetime.now().day).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "calls_more_that_5_minutes_count": callControl.objects.filter(bitrix_staff_id=user,
                                                                                  DURATION__gt='300',
                                                                                  DateCreate__year=datetime.now().year,
                                                                                  DateCreate__day=datetime.now().day).count(),
                    "total_Incoming_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='1',
                                                                       DateCreate__year=datetime.now().year,
                                                                       DateCreate__day=datetime.now().day).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "total_Incoming_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='1',
                                                                             DateCreate__year=datetime.now().year,
                                                                             DateCreate__day=datetime.now().day).count(),
                    "total_outgoing_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                       DateCreate__year=datetime.now().year,
                                                                       DateCreate__day=datetime.now().day).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "total_outgoing_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                             DateCreate__year=datetime.now().year,
                                                                             DateCreate__day=datetime.now().day).count(),
                    "total_missed_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='304',
                                                                     DateCreate__year=datetime.now().year,
                                                                     DateCreate__day=datetime.now().day).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "total_missed_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='304',
                                                                           DateCreate__year=datetime.now().year,
                                                                           DateCreate__day=datetime.now().day).count(),
                    "rejected_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                 DateCreate__year=datetime.now().year,
                                                                 DateCreate__week=datetime.now().day).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "rejected_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                       DateCreate__year=datetime.now().year,
                                                                       DateCreate__week=datetime.now().day).count(),

                    "busy_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                             DateCreate__year=datetime.now().year,
                                                             DateCreate__week=datetime.now().day).values('PHONE_NUMBER',
                                                                                                         'VOTE', 'COST',
                                                                                                         'DateCreate'),
                    "busy_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                   DateCreate__year=datetime.now().year,
                                                                   DateCreate__week=datetime.now().day).count(),
                }
                    for user in users
                }

                anlazing_task = {' '.join((user.first_name, user.last_name)): {
                    "tasks_deferred": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='6',
                                                                 CREATED_DATE__year=datetime.now().year,
                                                                 CREATED_DATE__day=datetime.now().day).values(
                        'TITLE', 'DESCRIPTION', 'DEADLINE', 'TIME_ESTIMATE'),
                    "tasks_deferred_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='6',
                                                                       CREATED_DATE__year=datetime.now().year,
                                                                       CREATED_DATE__day=datetime.now().day).count(),
                    "tasks_in_progress": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='3',
                                                                    CREATED_DATE__year=datetime.now().year,
                                                                    CREATED_DATE__day=datetime.now().day).values(
                        'TITLE', 'DESCRIPTION', 'DEADLINE', 'TIME_ESTIMATE'),
                    "tasks_in_progress_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='3',
                                                                          CREATED_DATE__year=datetime.now().year,
                                                                          CREATED_DATE__day=datetime.now().day).count(),
                    "tasks_needs_rework": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='7',
                                                                     CREATED_DATE__year=datetime.now().year,
                                                                     CREATED_DATE__day=datetime.now().day).values(
                        'TITLE', 'DESCRIPTION', 'DEADLINE', 'TIME_ESTIMATE'),
                    "tasks_needs_rework_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='7',
                                                                           CREATED_DATE__year=datetime.now().year,
                                                                           CREATED_DATE__day=datetime.now().day).count(),
                    "tasks_overdue": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='5',
                                                                CREATED_DATE__year=datetime.now().year,
                                                                CREATED_DATE__day=datetime.now().day).values(
                        'TITLE', 'DESCRIPTION', 'DEADLINE', 'TIME_ESTIMATE'),
                    "tasks_overdue_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='5',
                                                                      CREATED_DATE__year=datetime.now().year,
                                                                      CREATED_DATE__day=datetime.now().day).count(),
                } for user in users}

                anlazing_time = {' '.join((user.first_name, user.last_name)): {
                    "time": TimeControl.objects.filter(bitrix_staff_id=user, START_TIME__year=datetime.now().year,
                                                       START_TIME__day=datetime.now().day).values('TIME_LEAKS',
                                                                                                  'DURATION')
                } for user in users}

            elif select_report_type == 'Отчет о проделанной работе за неделю':
                anlazing_call = {' '.join((user.first_name, user.last_name)): {
                    "calls_less_that_30_seconds": callControl.objects.filter(bitrix_staff_id=user, DURATION__lt='30',
                                                                             DateCreate__year=datetime.now().year,
                                                                             DateCreate__week=datetime.now().isocalendar().week).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "calls_less_that_30_seconds_count": callControl.objects.filter(bitrix_staff_id=user,
                                                                                   DURATION__lt='30',
                                                                                   DateCreate__year=datetime.now().year,
                                                                                   DateCreate__week=datetime.now().isocalendar().week).count(),
                    "calls_more_that_5_minutes": callControl.objects.filter(bitrix_staff_id=user, DURATION__gt='300',
                                                                            DateCreate__year=datetime.now().year,
                                                                            DateCreate__week=datetime.now().isocalendar().week).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "calls_more_that_5_minutes_count": callControl.objects.filter(bitrix_staff_id=user,
                                                                                  DURATION__gt='300',
                                                                                  DateCreate__year=datetime.now().year,
                                                                                  DateCreate__week=datetime.now().isocalendar().week).count(),
                    "total_Incoming_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='1',
                                                                       DateCreate__year=datetime.now().year,
                                                                       DateCreate__week=datetime.now().isocalendar().week).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "total_Incoming_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='1',
                                                                             DateCreate__year=datetime.now().year,
                                                                             DateCreate__week=datetime.now().isocalendar().week).count(),
                    "total_outgoing_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                       DateCreate__year=datetime.now().year,
                                                                       DateCreate__week=datetime.now().isocalendar().week).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "total_outgoing_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                             DateCreate__year=datetime.now().year,
                                                                             DateCreate__week=datetime.now().isocalendar().week).count(),
                    "total_missed_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='304',
                                                                     DateCreate__year=datetime.now().year,
                                                                     DateCreate__week=datetime.now().isocalendar().week).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "total_missed_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_FAILED_CODE='304',
                                                                           DateCreate__year=datetime.now().year,
                                                                           DateCreate__week=datetime.now().isocalendar().week).count(),
                    "rejected_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                 DateCreate__year=datetime.now().year,
                                                                 DateCreate__week=datetime.now().isocalendar().week).values(
                        'PHONE_NUMBER', 'VOTE', 'COST', 'DateCreate'),
                    "rejected_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                       DateCreate__year=datetime.now().year,
                                                                       DateCreate__week=datetime.now().isocalendar().week).count(),

                    "busy_calls": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                             DateCreate__year=datetime.now().year,
                                                             DateCreate__week=datetime.now().isocalendar().week).values(
                        'PHONE_NUMBER',
                        'VOTE', 'COST',
                        'DateCreate'),
                    "busy_calls_count": callControl.objects.filter(bitrix_staff_id=user, CALL_TYPE='2',
                                                                   DateCreate__year=datetime.now().year,
                                                                   DateCreate__week=datetime.now().isocalendar().week).count(),
                } for user in users}
                anlazing_task = {' '.join((user.first_name, user.last_name)): {
                    "tasks_deferred": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='6',
                                                                 CREATED_DATE__year=datetime.now().year,
                                                                 CREATED_DATE__week=datetime.now().isocalendar().week).values(
                        'TITLE', 'DESCRIPTION', 'DEADLINE', 'TIME_ESTIMATE'),
                    "tasks_deferred_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='6',
                                                                       CREATED_DATE__year=datetime.now().year,
                                                                       CREATED_DATE__week=datetime.now().isocalendar().week).count(),
                    "tasks_in_progress": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='3',
                                                                    CREATED_DATE__year=datetime.now().year,
                                                                    CREATED_DATE__week=datetime.now().isocalendar().week).values(
                        'TITLE', 'DESCRIPTION', 'DEADLINE', 'TIME_ESTIMATE'),
                    "tasks_in_progress_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='3',
                                                                          CREATED_DATE__year=datetime.now().year,
                                                                          CREATED_DATE__week=datetime.now().isocalendar().week).count(),
                    "tasks_needs_rework": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='7',
                                                                     CREATED_DATE__year=datetime.now().year,
                                                                     CREATED_DATE__week=datetime.now().isocalendar().week).values(
                        'TITLE', 'DESCRIPTION', 'DEADLINE', 'TIME_ESTIMATE'),
                    "tasks_needs_rework_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='7',
                                                                           CREATED_DATE__year=datetime.now().year,
                                                                           CREATED_DATE__week=datetime.now().isocalendar().week).count(),
                    "tasks_overdue": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='5',
                                                                CREATED_DATE__year=datetime.now().year,
                                                                CREATED_DATE__week=datetime.now().isocalendar().week).values(
                        'TITLE', 'DESCRIPTION', 'DEADLINE', 'TIME_ESTIMATE'),
                    "tasks_overdue_count": TaskControl.objects.filter(bitrix_staff_id=user, STATUS='5',
                                                                      CREATED_DATE__year=datetime.now().year,
                                                                      CREATED_DATE__week=datetime.now().isocalendar().week).count(),
                } for user in users}

                anlazing_time = {' '.join((user.first_name, user.last_name)): {
                    "time": TimeControl.objects.filter(bitrix_staff_id=user, START_TIME__year=datetime.now().year,
                                                       START_TIME__week=datetime.now().isocalendar().week).values(
                        'TIME_LEAKS', 'DURATION')
                } for user in users}

            if select_departament == "Отдел не выбран":
                if select_type_staff == "Сотрудник не выбран":
                    prompt = [
                        """
                        \nВступай в роли бота, который пишет {0} от третьего лица (от лица компании Эркью) по сотрудникам:{1}.
                        \nВ отчёте должна содержаться детальная информация о эффективности работы cотрудников учитывая данные и должность сотрудника:
                        \nанализ задач сотрудников:{2}, анализ времени работы сотрудников:{3}.
                        \nОтчёт должен содержать заголовки:
                        \nУспехи:детальная информация о преимуществах сотрудников {1} за {0}.
                        \nОшибки:детальная информация о недостатках работы сотрудников {1} за {0}.
                        \nОбщий комментарий:выводы по работе сотрудников {1}.
                        \nВозможные риски:укажи возможные риски эффективности работы сотрудников организации на основе исторических данных:анализ задач сотрудника:{2},
                        \nанализ времени работы сотрудника:{3}.
                        \nРекомендации по улучшению работы:какие статьи, книги, документацию должены прочитать сотрудники {1} организации, укажи источники.
                        \nСледуй всем требованиям формирования отчёта для эффективности и контроля работы сотрудников организации и предоставляй точные числовые значения статистики работы сотруднка.
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
                    ]

                    # add_new_report_emps = Attendance_Report(
                    #     name_report=select_report_type,
                    #     description=response.text
                    # )
                else:
                    prompt = [
                        """
                        \nВступай в роли бота, который пишет {0} от третьего лица (от лица компании Эркью) по сотруднику {1} с должностью {4} в {5}.
                        \nВ отчёте должна содержаться детальная информация о
                        \nэффективности работы cотрудника учитывая данные и должность сотрудника: анализ задач сотрудника:{2}, анализ времени работы сотрудника:{3}.
                        \nОтчёт должен содержать заголовки:
                        \nУспехи: детальная информация о преимуществах сотрудника {1} за {0}.
                        \nОшибки: детальная информация о недостатках работы сотрудника {1} за {0}.
                        \nОбщий комментарий: выводы по работе сотрудника {1}.
                        \nРекомендации по улучшению работы:  какие статьи, книги, документацию должен прочитать сотрудник {1} организации, укажи источники.
                        \nВозможные риски: укажи возможные риски эффективности работы сотрудника организации на основе исторических данных: анализ задач сотрудника:{2},
                        \nанализ времени работы сотрудника:{3}.
                        \nСледуй всем требованиям формирования отчёта для эффективности и контроля работы сотрудника организации и предоставляй точные числовые значения статистики работы сотруднка.
                        \nИнформация должна быть подробно описана в заголовках: Успехи:, Ошибки:, Общий комментарий:, Рекомендации по улучшению работы:, Возможные риски:.
                        \nФормат вывода заголовков отчёта:
                        \nУспехи:[Успех_1, Успех_2 ... Успех_N],
                        \nОшибки:[Ошибки_1, Ошибки_2 ... Ошибки_N],
                        \nРекомендации по улучшению работы:[Рекомендация_1, Рекомендация_2 ... Рекомендация_N],
                        \nОбщий комментарий:[Общая информация].
                        \nВозможные риски:[риск_1, риск_2 ... риск_N].\n\n\n
                        """.format(select_report_type, select_type_staff, anlazing_task, anlazing_time,
                                   customer.WORK_POSITION, customer.WORK_DEPARTMENT),
                    ]

            elif select_departament == "Отдел поддержки клиентов":
                if select_type_staff == "Сотрудник не выбран":
                    prompt = [
                        """
                        \nВступай в роли бота, который пишет {0} от третьего лица (от лица компании Эркью) по сотрудникам отдела поддержки клиентов:{1}.
                        \nВ отчёте должна содержаться детальная информация о эффективности работы cотрудников отдела поддержки клиентов учитывая данные и должность сотрудника:
                        \nанализ задач сотрудников:{2}, анализ времени работы сотрудников: {3}, анализ звонков обработанные сотрудниками:{4}.
                        \nОтчёт должен содержать заголовки:
                        \nУспехи:детальная информация о преимуществах сотрудников {1} за {0}.
                        \nОшибки:детальная информация о недостатках работы сотрудников {1} за {0}.
                        \nОбщий комментарий:выводы по работе сотрудников {1}.
                        \nВозможные риски:укажи возможные риски эффективности работы сотрудников организации на основе исторических данных:анализ задач сотрудника:{2},
                        \nанализ времени работы сотрудника:{3}, анализ звонков обработанные сотрудниками:{4}.
                        \nРекомендации по улучшению работы:какие статьи, книги, документацию должены прочитать сотрудники {1} организации, укажи источники.
                        \nСледуй всем требованиям формирования отчёта для эффективности и контроля работы сотрудников организации и предоставляй точные числовые значения статистики работы сотруднка.
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
                    ]
                else:
                    prompt = [
                        """
                        \nВступай в роли бота, который пишет {0} от третьего лица (от лица компании Эркью) по сотрудникам отдела поддержки клиентов c должность {5}.
                        \nВ отчёте должна содержаться детальная информация о эффективности работы cотрудников отдела поддержки клиентов учитывая данные и должность сотрудника:
                        \nанализ задач сотрудников:{2}, анализ времени работы сотрудников: {3}, анализ звонков обработанные сотрудниками:{4}.
                        \nОтчёт должен содержать заголовки:
                        \nУспехи:детальная информация о преимуществах сотрудников {1} за {0}.
                        \nОшибки:детальная информация о недостатках работы сотрудников {1} за {0}.
                        \nОбщий комментарий:выводы по работе сотрудников {1}.
                        \nВозможные риски:укажи возможные риски эффективности работы сотрудников организации на основе исторических данных:анализ задач сотрудника:{2},
                        \nанализ времени работы сотрудника:{3}, анализ звонков обработанные сотрудниками:{4}.
                        \nРекомендации по улучшению работы:какие статьи, книги, документацию должены прочитать сотрудники {1} организации, укажи источники.
                        \nСледуй всем требованиям формирования отчёта для эффективности и контроля работы сотрудников организации и предоставляй точные числовые значения статистики работы сотруднка.
                        \nИнформация должна быть подробно описана в заголовках: Успехи:, Ошибки:, Общий комментарий:, Рекомендации по улучшению работы:, Возможные риски:.
                        \nФормат вывода заголовков отчёта:
                        \nУспехи:[сотрудник_1, cотрудник_2 ... сотрудник_N],
                        \nОшибки:[сотрудник_1, cотрудник_2 ... сотрудник_N],
                        \nРекомендации по улучшению работы:[сотрудник_1, cотрудник_2 ... сотрудник_N],
                        \nОбщий комментарий:[сотрудник_1, cотрудник_2 ... сотрудник_N],
                        \nВозможные риски:[риск_1, риск_2 ... риск_N].\n\n\n
                        """.format(
                            select_report_type, customer, anlazing_task, anlazing_time, anlazing_call,
                            customer.WORK_POSITION
                        )
                    ]

            # print(prompt)

            response = model.generate_content(prompt)

            staff_add = CustomUser.objects.filter(
                first_name=select_type_staff_split[0],
                last_name=select_type_staff_split[1],
                user_type=2
            ).values_list("id", flat=True)[0]

            # add_new_report_emp = Attendance_Report(
            #     name_report=select_report_type,
            #     description=response.text,
            #     staff_id=str(staff_add)
            # )

            description = response.text
            staff_id = str(staff_add)

            # add_new_report.save()
            # prompt.clear()

            staff = CustomUser.objects.filter(user_type=2)

            import re
            print(description)
            descriptions = re.sub('', '', description).replace('\n', " ").split('  ')
            # descriptions = [section.strip() for section in re.sub('', '', description).replace('\n', " ").split('  ') if section.strip()]
            dict = [line.replace('**', '') for line in descriptions]

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

        # add_new_report_PDF = Customer(
        #     name_report=select_report_type,
        # )
        # add_new_report_PDF.save()

        # Extract chatbot replies from the response
        # chatbot_replies = [message['message']['content'] for message in response['choices'] if
        #                    message['message']['role'] == 'assistant']

        # Append chatbot replies to the conversation
        # for reply in chatbot_replies:
        #     conversation.append({"role": "assistant", "content": reply})

        # Update the conversation in the session
        # request.session['conversation'] = conversation

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
    print(content)

    return render(request, "Hod/report_create.html", content)
