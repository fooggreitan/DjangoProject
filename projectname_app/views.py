from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from app.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import CustomUser

def BASE(request):
    return render(request, 'base.html')

def LOGIN(request):
    return render(request, 'login.html')

def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user!=None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1': return redirect('hod_home')
            elif user_type == '2': return redirect('staff_home')
            elif user_type == '3': return HttpResponse('This Emploes Panel')
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
    user = CustomUser.objects.get(id = request.user.id)
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
            customuser = CustomUser.objects.get(id = request.user.id)

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

def fORGOTPASSWORD(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'))
        if user != None:
            messages.success(request, 'Вы крут!')
        else:
            messages.error(request, 'Вы не зарегистрированы')
            return redirect('login')
    else:
        return redirect('forgotPassword')

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