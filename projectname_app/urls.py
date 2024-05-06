from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views, Hod_Views, Staff_Views, Emploes_views

from .Hod_Views import app_render_pdf_view

urlpatterns = [

    # path("admin/", admin.site.urls),
    path('base/', views.BASE, name='base'),
    path("admin/", admin.site.urls),
    # path('', include('app.urls', namespace='app')),

    # path('Hod/hello/', include('a pp.urls', namespace='app')),
    # path('Hod/add_report.html', AppListView.as_view(), name='list-view'),
    # path('test/', render_pdf_view, name='test-view'),
    # path('pdf/<pk>/', app_render_pdf_view, name='pdf-view'),
    # path('Hod/Report', AppListView.as_view(), name='list-view'),

    path('pdf/<str:id>', app_render_pdf_view, name='pdf-view'),

    # login
    path('', views.LOGIN, name='login'),
    path('Register/', views.REGISTER, name='register'),
    path('ForgotPassword/', views.fORGOTPASSWORD, name='forgotPassword'),
    path('PasswordRecovery/', views.PASSWORDRECOVERY, name='passwordRecovery'),

    path('saveNewPassword', views.saveNewPassword, name='saveNewPassword'),
    path('doPasswordRecovery', views.doPasswordRecovery, name='doPasswordRecovery'),
    path('doRegistr', views.doRegistr, name='doRegistr'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),

    # profile
    path('Profile', views.PROFILE, name='profile'),

    path('Hod/Report#', Hod_Views.chatbot_view, name='chatbot_view'),
    path('Hod/Reports#', Hod_Views.create_new_report, name='create_new_report'),
    path('Hod/ReportCreate', Hod_Views.REPORTCREATE, name='report_create'),

    path('Hod/Report', Hod_Views.ADD_REPORT, name='add_report'),
    path('Hod/Report/DeleteReport/<str:id>', Hod_Views.DELETEREPORT, name='report-delete'),

    path('Hod/TaskControl', Hod_Views.TASKCONTROL, name='taskControl_view'),
    path('Hod/TimeControl', Hod_Views.TIMECONTROL, name='timeControl_view'),
    path('Hod/СallControl', Hod_Views.CALLCONTROL, name='callControl_view'),

    # update profile
    path('Profile/update', views.PROFILE_UPDATE, name='profile_update'),
    path('Hod/Staff/about_profile', Hod_Views.ABOUT_PROFILE, name='about_profile'),

    path('Hod/Home', Hod_Views.HOME, name='hod_home'),
    path('Hod/Deal', Hod_Views.VIEW_DEAL, name='view_deal'),
    path('Hod/Case', Hod_Views.VIEW_CASE, name='view_case'),

    path('Hod/Bitrix_24', Hod_Views.BITRIX, name='add_bitrix24'),
    path('Hod/Bitrix_24/NewWebhook', Hod_Views.NEW_WEBHOOK, name='add_bitrix24_new_webhook'),

    # path('Hod/Report', Hod_Views.chatbot, name='chatGPT_add_report'),

    path('Hod/Staff/Add', Hod_Views.ADD_STAFF, name='add_staff'),

    path('Hod/Staff/View', Hod_Views.VIEW_STAFF, name='view_staff'),

    path('Hod/Staff/Edit/<str:id>', Hod_Views.EDIT_STAFF, name='edit_staff'),
    path('Hod/Staff/Delete/<str:admin>', Hod_Views.DELETE_STAFF, name='delete_staff'),

    # Для сотрудников
    path('Staff/Notification', Staff_Views.NOTIFICATION, name='staff_notification'),
    path('Staff/mark_as_done/<str:status>', Staff_Views.STATUSNOTIFICATION, name='staff_STATUS'),

    path('Staff/Task/View', Hod_Views.VIEW_STAFF_TASK, name='view_task'),

    path('Staff/Home', Staff_Views.HOME, name='staff_home'),
    path('Hod/Task/View', Hod_Views.VIEW_TASK, name='view_task'),
    path('Hod/Task/Attendance', Hod_Views.VIEW_ATT, name='view_attendance'),

    # Уведомления
    path('Hod/Staff/Send_Notification', Hod_Views.STAFF_SEND_NOTIFICATION, name='staff_send_notification'),
    path('Hod/Staff/save_notification', Hod_Views.STAFF_SAVE_NOTIFICATION, name='staff_save_notification'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)