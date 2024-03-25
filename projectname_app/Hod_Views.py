from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import CustomUser, Staff, Task, Staff_Notification, Attendance_Report
from django.contrib import messages

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView
from app.models import Customer

from openai import ChatCompletion
import openai


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

    response = 'Привет'

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
        # user_input = request.POST.get('textPostSelect')
        # print(user_input)

        customer = ""
        staff = Customer.objects.values('name')
        for i in staff: customer += i['name']

        print(customer)
        print(select_report_type)
        print(select_type_staff)

        if select_report_type != 'Отчёт не выбран':
            prompts = []

            '''Начальный системный промт'''

            prompts.append({"role": "system", "content": """
                Ты являешься ботом который формирует отчёты от третьего лица (от лица компании Эркью)
                Ты должен следовать всем требованиям формирования отчётов для эффективности и контроля
                работы сотрудников организации. Вывод информации должен содержать только основную часть успехов
                сорудников, ошибок сотрудников и рекомендации по улучшению их работы.
            """})

            '''Промт сотрудника за месяц'''

            if select_type_staff == "Сотрудник не выбран":
                prompts.append({"role": "user", "content": "Cделай {0} включая каждого сотрудников {1}".format(
                    select_report_type,
                    customer
                )})
            else:
                prompts.append({"role": "user", "content": "Cделай {0} по сотруднику {1}".format(
                    select_report_type,
                    select_type_staff
                )})

            # Append conversation messages to prompts
            # prompts.extend(conversation)

            # Set up and invoke the ChatGPT model

            response = openai.ChatCompletion.create(
                model="ft:gpt-3.5-turbo-0613:personal::7wZAALHG",
                messages=prompts,
                api_key="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",
                max_tokens=1200,
                temperature=0.2,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0.5
            )

            res_Bot = response['choices'][0]['message']['content']

            print(res_Bot)

            '''' Создание отчёта'''

            add_new_report = Attendance_Report(
                name_report=select_report_type,
                description=res_Bot
            )
            add_new_report.save()

            prompts.clear()

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

def fetch_pdf_resources(uri, rel):
    if uri.find(settings.MEDIA_URL) != -1:
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    elif uri.find(settings.STATIC_URL) != -1:
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ''))
    else:
        path = None
    return path

def app_render_pdf_view(request, id):
    data = Attendance_Report.objects.get(id=id)
    template_path = 'report/pdf2.html'
    context = {'pdf': data}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html.encode("UTF-8"), dest=response, encoding="UTF-8", link_callback=fetch_pdf_resources)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

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
