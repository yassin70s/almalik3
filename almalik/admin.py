from main.admin import *
from . import models
from django.utils.html import format_html
from django.urls import path,reverse
from django.utils.timezone import datetime



class BalanceAdmin(ModelAdmin):
    list_display = ["datetime_add","balance_type","balance_total","balance_receive","balance_spend","balance_activitys"]
    def get_queryset(self, request):
        #if not request.user.is_superuser:
        return super().get_queryset(request)
    def balance_total(self,obj):
        balance_receive = 0
        for ba_re in models.BalanceReceive.objects.filter(balance=obj).filter(statu="OK"):
            balance_receive += ba_re.amount
        balance_spend = 0
        for ba_sp in models.BalanceSpend.objects.filter(balance=obj):
            balance_spend += ba_sp.amount

        return (balance_receive - balance_spend)  + 100
    def balance_receive(self,obj):
        receive = 0
        for ba_re in models.BalanceReceive.objects.filter(balance=obj).filter(statu="OK"):
            receive += ba_re.amount
        return receive
    def balance_spend(self,obj):
        spend = 0
        for ba_sp in models.BalanceSpend.objects.filter(balance=obj):
            spend += ba_sp.amount
        return spend
    def balance_activitys(self,obj):
        rece = []
        for ba_re in models.BalanceReceive.objects.filter(balance=obj).filter(statu="1"):
            rece += [{
                "id":ba_re.id,
                "receive_type":ba_re.receive_type.name,
                "number":ba_re.number,
                "amount":ba_re.amount,
                "time":ba_re.datetime_add.time(),
                "date":ba_re.datetime_add.date(),
            }]
        return rece
    



class BalanceReceiveAdmin(ModelAdmin):
    pass


class ProjectOfferInline(StackedInline):
    model = models.ProjectOffer
    extra = 1
class ProjectStartInline(StackedInline):
    model = models.ProjectStart
    max_num = 1
    #readonly_fields = ["p"]
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "projectoffer":
            kwargs["queryset"] = models.ProjectOffer.objects.filter(project=self.obj)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_extra(self, request, obj, **kwargs):
        self.obj = obj
        return 1
    
class ProjectJobInline(StackedInline):
    model = models.ProjectJob
    extra = 1
class ProjectEndInline(StackedInline):
    model = models.ProjectEnd
    extra = 1
    max_num = 1
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "projectstart":
            kwargs["queryset"] = models.ProjectStart.objects.filter(project=self.obj)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_extra(self, request, obj, **kwargs):
        self.obj = obj
        return super().get_extra(request, obj, **kwargs)
class ProjectDdownloadInline(TabularInline):
    model = models.ProjectDdownload
    extra = 0
    readonly_fields = ["projectend","user"]
class ProjectCodeInline(StackedInline):
    model = models.ProjectCode
    extra = 1
class ProjectStopInline(StackedInline):
    model = models.ProjectStop
    extra = 1
    max_num = 1
class ProjectUnAcceptedInline(StackedInline):
    model = models.ProjectUnAccepted
    extra = 1
    max_num = 1

class ProjectAppInline(TabularInline):
    model = models.ProjectApp
    extra = 1
    max_num = 1




class ProjectAdmin(ModelAdmin):
    list_display = ["department","id","user","title","datetime_add","price_min","price_max","days","project_url"]
    actions = ["runserver"]

    def project_url(self,obj):
        start = models.ProjectStart.objects.get(project=obj)
        return format_html(f"<a href='http://127.0.0.1:{obj.id}'>fffffffffff</a>")
   
    def title(self,obj):
        return obj.name
    def _statu(self,obj):
        project_offers = models.ProjectOffer.objects.filter(project=obj)
        project_unaccepteds = models.ProjectUnAccepted.objects.filter(project=obj)
        project_start = models.ProjectStart.objects.filter(project=obj)
        project_end = models.ProjectEnd.objects.filter(project=obj)
        project_job = models.ProjectJob.objects.filter(project=obj)
        project_stop = models.ProjectStop.objects.filter(project=obj)
        text = ""
        tag = ""
        body_name = ""
        context = {}
        if project_unaccepteds.exists():
            text = "تم رفض المشروع"
            tag = "danger"
            body_name = "body_1"
            context.update(
            )
        elif project_stop.exists():
            text = "تم الايقاف"
            tag = "dark"
            body_name = "body_2"
        elif project_offers.exists():

            if project_start.exists():
                if project_end.exists():
                    text = "تم إنجاز المشروع"
                    tag = "success"
                    body_name = "body_3"
                    project_end = project_end.get(project=obj)
                    project_ddownload = models.ProjectDdownload.objects.filter(project=obj)
                    context = {
                        "project_end":{
                            "id":project_end.id,
                            "file_url":project_end.file.url,
                        },
                        "project_ddownload":{
                            "count":project_ddownload.count(),
                        },

                    }
                else:
                    text = "المشروع قيد التنفيذ"
                    tag = "secondary"
                    body_name = "body_4"
                    project_start = project_start.get(project=obj)
                    last_days = (datetime.now().date().toordinal()  - project_start.datetime_add.date().toordinal())
                    print(datetime.now().date().toordinal(),datetime.now() ,project_start.datetime_add)
                    context = {
                        "last_days":last_days,
                        "rate":int(last_days / (project_start.period)*100),
                    }
            else:
                
                text = "المشروع في انتظار البدء"
                tag = "warning"
                body_name = "body_5"
                
        else:
            text = "المشروع قيد المراجعة"
            tag = "info"
            body_name = "body_6"
        #return self.get_statu(text,)
        return {"header":format_html(f"""<span class="badge bg-{tag}">{text}</span>"""),"body_name":body_name,"context":context}

    def _start(self,obj):
        a = f"<a href=''>{5}</a>"
        return format_html()
    def runserver(self,request,queryset):
        import os
        for qs in queryset:
            start = models.ProjectStart.objects.get(project=qs)
            os.system(f"python {os.path.join(start.path,'runserver.py')}")

    def project_offers(self,obj):
        _project_offers = []
        for pr_offer in models.ProjectOffer.objects.filter(project=obj):
            offer_price = 0
            offer_jobs = []
            offer_period = 0
            for of_jobs in models.OfferJob.objects.filter(offer=pr_offer.offer):
                
                offer_jobs += [{
                    "name":of_jobs.job.name,
                    "price":of_jobs.price,
                    "period":of_jobs.period,
                }]
                offer_price += of_jobs.price
                offer_period += of_jobs.period
            _project_offers += [{
                "id":pr_offer.id,
                "offer_name":pr_offer.offer.name,
                "offer_jobs":offer_jobs,
                "offer_price":offer_price,
                "offer_period":offer_period
                
            }]
        return _project_offers
   

    def app_url(self,obj):
        project_app = models.ProjectApp.objects.filter(project=obj)
        project_app_url = ""
        

        return ""


    inlines = [
        ProjectOfferInline,
        ProjectUnAcceptedInline,
        ProjectStartInline,
        ProjectJobInline,
        ProjectEndInline,
        ProjectDdownloadInline,
        ProjectStopInline,
        ProjectCodeInline,
        ProjectAppInline,
        ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs







class UserContactAdmin(ModelAdmin):
    list_display = ["user","contact"]


    




class NoticeUserAdmin(ModelAdmin):
    list_display = ["id","profile","message","time","delete_url","is_view"]
    def profile(self,obj):
        return ""
    def message(self,obj):
        content = obj.notice.content
        return f"{content}"
    def time(self,obj):
        d = obj.notice.datetime.date()
        t = obj.notice.datetime.time()

        return f"{d.month} - {d.day} | {t.hour}:{t.minute}:{t.second}"
    def delete_url(self,obj):
        return reverse(f"api:{self.opts.app_label}_noticeuser_delete",kwargs={"object_id":obj.id})
    
    def get_queryset(self, request):
        if not request.user.username == "yassin":
            return super().get_queryset(request).filter(user=request.user)
        return super().get_queryset(request)
    
  