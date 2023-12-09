
import os
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from weasyprint import HTML, CSS
from django.template.loader import render_to_string





    
from django.contrib.auth.models import Permission

def get_permissions(models=[],permissions=[]):
        codenames = []
        for model in models:
            for permission in permissions:
                codenames += [f"{permission}_{model._meta.model_name}"]
        return Permission.objects.filter(codename__in = codenames)






def render_to_pdf(request, template_name="",pdf_name="test",context={},styles=[]):
    html_string = render_to_string(template_name, context)

    styles = CSS(settings.STATIC_ROOT + '/vendor/adminlte/css/adminlte_ar.min.css')
    

    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
        os.path.join(settings.MEDIA_ROOT,f"{pdf_name}.pdf"),
         presentational_hints=True,
        stylesheets=[styles], 
    )
    pdf_url = os.path.join(settings.MEDIA_URL,f"{pdf_name}.pdf")
    pdf_viewer_url = settings.STATIC_URL + f"jsPDF-master/examples/PDF.js/web/viewer.html?file={pdf_url}"
    return HttpResponseRedirect(pdf_viewer_url)


def date_format(date):
    return f"{date.year}/{date.month}/{date.day}"


