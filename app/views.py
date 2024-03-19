from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views.generic import ListView
from .models import Customer

class AppListView(ListView):
    model = Customer
    template_name = 'Hod/add_report.html'

def app_render_pdf_view(request, *args, **kwargs):
    PDF_report = kwargs.get('pk')
    app_report = get_object_or_404(Customer, pk=PDF_report)

    template_path = 'report/pdf2.html'
    context = {'app_report': app_report}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# def render_pdf_view(request):
#     pass
#     # template_path = 'report/pdf1.html' #шаблон
#     # context = {'myvar': 'this is your template context'} #передеча в шаблон
#     # # Create a Django response object, and specify content_type as pdf
#     # response = HttpResponse(content_type='application/pdf')
#     # # if download:
#     # # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#     # # if display:
#     # response['Content-Disposition'] = 'filename="report.pdf"'
#     # # find the template and render it.
#     # template = get_template(template_path)
#     # html = template.render(context)
#     #
#     # # create a pdf
#     # pisa_status = pisa.CreatePDF(
#     #    html, dest=response)
#     # # if error then show some funny view
#     # if pisa_status.err:
#     #    return HttpResponse('We had some errors <pre>' + html + '</pre>')
#     # return response