from .views import app_render_pdf_view
from django.urls import path, include
from django.contrib import admin

app_name = 'app'  # зарегистрированное имя

urlpatterns = [
    # path("admin/", admin.site.urls),
    # path('', include('projectname_app.urls')),
    # path('', AppListView.as_view(), name='list-view'),
    # path('test/', render_pdf_view, name='test-view'),
    path('pdf/<pk>/', app_render_pdf_view, name='pdf-view'),
]
