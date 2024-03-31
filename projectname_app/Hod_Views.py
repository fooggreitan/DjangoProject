from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import CustomUser, Staff, Task, Staff_Notification, Attendance_Report
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

import os


@login_required(login_url='/')
def HOME(request):
    staff_count = Staff.objects.all().count()

    staff_male = Staff.objects.filter(gender='Male').count()
    staff_female = Staff.objects.filter(gender='Female').count()

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
    staff = Staff.objects.all()
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


def chatbot_view(request, *args, **kwargs):
    print(request)
    # conversation = request.session.get('conversation', [])
    if request.method == 'POST':
        select_report_type = request.POST.get('select_type_report')
        select_type_staff = request.POST.get('select_type_staff')

        select_type_staff_split = select_type_staff.split()

        # user_input = request.POST.get('textPostSelect')
        # print(user_input)

        customer = ""

        staff = CustomUser.objects.filter(id__in=Staff.objects.values_list('admin_id', flat=True)).values('first_name', 'last_name')

        for i in staff:
            customer += "{0} {1} \n".format(i['first_name'], i['last_name'])

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

            if select_type_staff == "Сотрудник не выбран":

                prompt_parts = [
                    """
                    \nТы являешься ботом который формирует отчёт {0} от третьего лица (от лица компании Эркью) по сотрудникам: {1} и нужно описать поддробно и ФИО сотрудника не нужно выделять жирным шрифтом.
                    \nТы должен следовать всем требованиям формирования отчётов для эффективности и контроля сотрудников организации.
                    \nВ отчёте должно содержаться длинная информация о сотруднике.
                    \nОтчёт содержит заголовки: **Успехи:**, **Ошибки:**, **Рекомендации по улучшению работы:** и **Общий комментарий:**.
                    \nИнформация в заголовках **Успехи:**, **Ошибки:**, **Рекомендации по улучшению работы:** и **Общий комментарий:** подробно описана.\n\n\n
                    """.format(select_report_type, customer),
                ]

                print(prompt_parts)

                response = model.generate_content(prompt_parts)

                add_new_report = Attendance_Report(
                    name_report=select_report_type,
                    description=response.text
                )
            else:

                prompt_parts = [
                    """
                    \nТы являешься ботом который формирует отчёт {0} от третьего лица (от лица компании Эркью) по сотруднику {1}.
                    \nТы должен следовать всем требованиям формирования отчётов для эффективности и контроля.
                    \nВ отчёте должно содержаться длинная информация о сотруднике.
                    \nОтчёт содержит заголовки: **Успехи:**, **Ошибки:**, **Рекомендации по улучшению работы:** и **Общий комментарий:**.
                    \nИнформация в заголовках **Успехи:**, **Ошибки:**, **Рекомендации по улучшению работы:** и **Общий комментарий:** подробно описана.\n\n\n
                    """.format(select_report_type, select_type_staff),
                ]

                response = model.generate_content(prompt_parts)

                staff_add = CustomUser.objects.filter(
                    first_name=select_type_staff_split[0],
                    last_name=select_type_staff_split[1]
                ).values_list("id", flat=True)[0]

                add_new_report = Attendance_Report(
                    name_report=select_report_type,
                    description=response.text,
                    staff_id=str(staff_add)
                )

            add_new_report.save()

            # prompt_parts.clear()

            messages.success(request, "Вы успешно создали отчёт!")
            return redirect('add_report')
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
    data = Attendance_Report.objects.get(id=id)

    json_dict = {
        "progress" : '',
        'error': '',
        'recommendations': '',
        'comment': ''
    }

    import re

    dict = re.sub('\d', '', Attendance_Report.objects.filter(id=id).values('description')[0].get('description')).replace('\n', ' ').split("  ")

    for i in range(len(dict)):
        if dict[i] == '**Успехи:**':
            json_dict['progress'] = dict[i + 1].replace('.', '.\n')
        elif dict[i] == '**Ошибки:**':
            json_dict['error'] = dict[i + 1].replace('.', '.\n')
        elif dict[i] == '**Рекомендации по улучшению работы:**':
            json_dict['recommendations'] = dict[i + 1].replace('.', '.\n')
        elif dict[i] == '**Общий комментарий:**':
            json_dict['comment'] = dict[i + 1].replace('.', '.\n')

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
#         content = {
#             "response": response
#         }
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
