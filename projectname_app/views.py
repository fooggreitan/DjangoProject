from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import CustomUser, Staff


def BASE(request):
    return render(request, 'base.html')


def LOGIN(request):
    return render(request, 'login.html')


def fORGOTPASSWORD(request):
    return render(request, 'forgotPassword.html')


def REGISTER(request):
    return render(request, 'register.html')


def PASSWORDRECOVERY(request):
    return render(request, 'passwordRecovery.html')

def saveNewPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if confirm_password == password:
            user = CustomUser.objects.filter(email=email).first()
            user.set_password(password)
            user.save()
            messages.success(request, 'Вы успешно восстановили пароль')
            return redirect('login')
        else:
            messages.error(request, 'Пароль введен неверно!')
            return redirect('passwordRecovery')
    else:
        messages.error(request, 'Вы ничего не ввели!')
        return redirect('passwordRecovery')

def doPasswordRecovery(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            context = {"email": email}
            return render(request, 'passwordRecovery.html', context)
        else:
            messages.error(request, 'Электронная почта неверна!')
            return redirect('forgotPassword')
    else:
        messages.error(request, 'Вы ничего не ввели!')
        return redirect('forgotPassword')

def doRegistr(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if confirm_password == password:
            user = CustomUser.objects.filter(email=email).first()
            if user and user.password == '':
                if request.POST.get('select_type_role') == 'Сотрудник':
                    user.user_type = 2
                else:
                    user.user_type = 1

                user.set_password(password)
                user.save()
                messages.success(request, 'Вы успешно зарегистрировались')
                return redirect('login')
            else:
                messages.error(request, 'Электронная почта и пароль неверны!')
                return redirect('register')
        else:
            messages.error(request, 'Вы ввели неправильный пароль!')
            return redirect('register')
    else:
        messages.error(request, 'Электронная почта и пароль неверны!')
        return redirect('register')

def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'),
                                         password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('hod_home')
            elif user_type == '2':
                return redirect('staff_home')
        else:
            messages.error(request, 'Электронная почта и пароль неверны!')
            return redirect('login')
    else:
        messages.error(request, 'Электронная почта и пароль неверны!')
        return redirect('login')

def doLogout(request):
    logout(request)
    return redirect('login')

def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        "user": user,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # email = request.POST.get('email')
        # username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            customuser = CustomUser.objects.get(id=request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name

            if password != None and password != "": customuser.set_password(password)
            if profile_pic != None and profile_pic != "": customuser.profile_pic = profile_pic

            customuser.save()
            messages.success(request, 'Ваш профиль обновлен!')
            return redirect('profile')
        except:
            messages.error(request, 'Ошибка ')
    return render(request, 'profile.html')

# def app_render_pdf_view(request, *args, **kwargs):
#     report_pdf = kwargs.get('pk')
#     app_report = get_object_or_404(Customer, pk=report_pdf)
#     template_path = 'Hod/pdf2.html'
#     context = {'app_report': app_report}
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename="report.pdf"'
#     template = get_template(template_path)
#     html = template.render(context)
#
#     pisa_status = pisa.CreatePDF(
#         html, dest=response)
#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     return response