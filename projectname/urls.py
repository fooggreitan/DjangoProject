from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .import views, Hod_Views, Staff_Views, Emploes_views

urlpatterns = [

    path("admin/", admin.site.urls),
    path('base/', views.BASE, name='base'),

    #login
    path('',views.LOGIN, name='login'),
    path('forgotPassword',views.fORGOTPASSWORD, name='forgotPassword'),
    path('doLogin',views.doLogin, name='doLogin'),

    path('doLogout', views.doLogout, name='logout'),

    #profile
    path('Profile', views.PROFILE, name='profile'),

    # update profile
    path('Profile/update', views.PROFILE_UPDATE, name='profile_update'),
    path('Hod/Staff/about_profile', Hod_Views.ABOUT_PROFILE, name='about_profile'),

    # Hod panel
    path('Hod/Home', Hod_Views.HOME, name='hod_home'),
    path('Hod/Report', Hod_Views.ADD_REPORT, name='add_report'),

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

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)