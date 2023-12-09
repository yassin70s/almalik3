from main import admin

from django.utils.timezone import datetime
import json
from django.utils.dateparse import parse_date,parse_datetime
from . import utils
from django.http.response import JsonResponse
from django.urls import reverse,path
from django.contrib.admin.templatetags.admin_list import result_list


class DateTimeField:
    def __init__(self,spec,value={}):
        self.spec = spec
        self.value = value
    def field(self):
        return {"type":"DateTimeField",
                "name":self.spec.field_path,
                "value":{"lt":None,"gte":None},
                "attrs": {
                    #"read_only": false,
                    #"write_only": false,
                    "required": True,
                    "default": None,
                    #"allow_blank": false,
                    #"allow_null": false,
                    "style": {},
                    "label": self.spec.title,
                    "help_text": None,
                    "initial": [],
                    #"choices":choices,
                    #"max_length": 150,
                    #"min_length": null,
                    #"trim_whitespace": true
                }
        }
    def get_query(self):
        q = ""
        if not self.value["lt"] == None:
            q += f"{self.spec.field_path}__lt={self.value['lt']}&"
        if not self.value["gte"] == None:
            q += f"{self.spec.field_path}__gte={self.value['gte']}&"
        return q[:-1]

class ModelReport(admin.ModelAdmin):
    actions = None
    list_display_links = None
    title_report = None
    logo = None
    horizontal = False
    
    list_filter_report = {"datetime":DateTimeField}
    exclude_filter_report = {"datetime":None}

    
    margin = {"top":"","bottom":""}
    date_filter = False

    address_list = [
        "مجموعة ألوية النصر",
        "الشعبة الطبية",
    ]
    def get_size(self):
        if self.horizontal:
            return {"width":"210mm","height":"297mm"}
        else:
            return {"width":"297mm","height":"210mm"}

    def get_list_display(self, request):
        if request.GET and "e" in request.GET:
            return request.GET["e"]
        return super().get_list_display(request)
    def get_title_report(self,request):
        return self.title_report or f"تقرير {self.opts.verbose_name_plural}"

    def changelist_view(self, request, extra_context=None):
        from .utils import render_to_pdf
        
        styles = ["vendor/adminlte/css/adminlte_ar.min.css"]
        return render_to_pdf(
            request, 
            template_name = None or [
                f"report/{self.opts.app_label}/{self.opts.model_name}/change_list.html",
                f"report/{self.opts.app_label}/change_list.html",
                f"report/change_list.html",
            ],
            context = self.get_context_report(request),
            styles = styles,
            pdf_name=self.get_title_report(request),
        )
    
    def get_context_report(self,request):
        cl = self.get_changelist_instance(request)
        cl.formset = None
        filters = []
        specs = cl.filter_specs
        for spec in specs:
            
            if not spec.field_path in self.exclude_filter_report:
                filters += [{
                    "title":spec.title,
                    "choices":spec.choices(cl)
                }]
        
        
        if self.date_filter:
            datetime__lt = str(self.get_queryset(request).last().datetime)
            datetime__gte = str(self.get_queryset(request).first().datetime)
            if request.GET:
                if "datetime__lt" in request.GET and not request.GET["datetime__lt"] == None:
                    datetime__lt = request.GET["datetime__lt"]
                    print(type(datetime__lt))
                if "datetime__gte" in request.GET and not request.GET["datetime__gte"] == None:
                    datetime__gte = request.GET["datetime__gte"]

            date_filter = f"من: {utils.date_format(parse_datetime(datetime__gte).date())} - حتى: {utils.date_format(parse_datetime(datetime__lt).date())}"
        else:
            date_filter = None

        context = {
            "result_list" : result_list(cl),
            "list_filters":filters,
            "date_filter":date_filter,
            "title":f"{cl.title}",

            "logo":self.logo or "/static/reports/logo.jpg",
            "title_report": self.get_title_report(request),
            "address_list":self.address_list,
            "date_report":datetime.now().date(),

            "size":self.get_size(),
            "margin":self.margin,

            
        }
        return context
    def filters_report(self,request):
        cl = self.get_changelist_instance(request)
        cl.formset = None
        fields = []
        specs = cl.filter_specs
        data_fields = {}
        data = {}
        report_url = ""
        if request.method == "POST":
            print(333)
            data_fields = json.loads(request.body)
            for key,value in data_fields['data'].items():
                print(key,value)
                if key in self.list_filter_report:
                    for spec in specs:
                        if spec.field_path == key:
                            report_url += self.list_filter_report[key](spec=spec,value=value).get_query()
                elif not value == None:
                    if not value == "الكل":

                        report_url += "{}={}&".format(key,value)
         
            print("yyy",self.get_queryset(request).count())
            return JsonResponse(data={"report_url":"?" + report_url[:-1]})
        
        fields = self.filters_form_json(request,data_fields=data_fields)
        print(fields)
        return JsonResponse({"fields":fields},)
    def filters_form_json(self,request,data_fields={}):
        cl = self.get_changelist_instance(request)
        cl.formset = None
        fields = []
        specs = cl.filter_specs
        options = {}
        
        for spec in specs:
            print(spec.__dict__)
            choices = {}
            value = None
            type = "ChoiceField"
            if spec.field_path in data_fields:
                value = data_fields[spec.field_path]
            if spec.field_path in self.list_filter_report:
                fields+=[self.list_filter_report[spec.field_path](spec=spec,value=value).field()]
            else:
                for choice in spec.choices(cl):
                    choices[str(choice["display"])] = choice["display"]
                
                fields+=[{
                    "type":type,
                    "name":spec.field_path,
                    "value":value,
                    "attrs": {
                        #"read_only": false,
                        #"write_only": false,
                        "required": True,
                        "default": None,
                        #"allow_blank": false,
                        #"allow_null": false,
                        "style": {},
                        "label": spec.title,
                        "help_text": None,
                        "initial": [],
                        "choices":choices,
                        #"max_length": 150,
                        #"min_length": null,
                        #"trim_whitespace": true
                    }
                }]
        
        return fields
        
    def get_urls(self):
        return [path("filters/",self.filters_report)] + super().get_urls()

    def add_view(self, request, form_url="", extra_context=None):
        
        return super().add_view(request,form_url,extra_context)
        #return JsonResponse(data={
        #    "change_list_api_url":reverse(f"backend_site:{self.opts.app_label}_{self.opts.model_name}_changelist"),
       #})
    def get_list_filter(self, request):
        
        return super().get_list_filter(request)
   

class Site(admin.AdminSite):
    pass

site = Site(name="report")