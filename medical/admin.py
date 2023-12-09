from main.admin import *
from . import forms,models,tests

#tests.dd()

class EntryAdmin(ModelAdmin):
    save_on_top = True
    form = forms.EntryForm
    def has_change_permission(self, request, obj=None):
        return False
    #list_display_links=None
    #actions = None
    #list_per_page = 100
    search_fields=['profilemedical__name',"hospital__name"]
    #autocomplete_fields=['profilemedical']
    list_filter = ["profilemedical__supervisor_general__name","datetime"]
   
    #report_to_site_index = True
   
    #change_form_template = 'posts/entry_add_form.html'
     
    #change_list_template = 'posts/entry_change_list.html'
    filter_horizontal=['injury','disease','becauseinjury','procedure']
    fieldsets = (
        ('البيانات الرئيسية', {
            "fields": (
                'hospital','profilemedical','datetime',
            ),
        }),
        ('بيانات الدخول', {
            "fields": (
                'entry_type','back','number_notification','diagnosi_type','injury','disease','becauseinjury',
            ),
        }),
        
        ('الإجراءات الطبية', {
            "fields": (
                'procedure','recipe',
            ),
        }),
        ('النتيجة النهائية', {
            "fields": (
                'result','period_digg','hospital_turn','date_back','report_death',
            ),
        }),
    )
    @display(description='الاسم')
    def _profilemedical_name(self,obj):
        return obj.profilemedical.name
    @display(description='الكنية')
    def _profilemedical_name_2(self,obj):
        return obj.profilemedical.name_2
    @display(description='المشرف العام')
    def _profilemedical_supervisor_general(self,obj):
        return obj.profilemedical.supervisor_general.name
    @display(description='المشرف المباشر')
    def _profilemedical_supervisor_direct(self,obj):
        return obj.profilemedical.supervisor_direct.name
    @display(description="التشخيص")
    def diagnosi(self,obj):
        diagnositypes = self.model.DiagnosiTypes
        _diagnosi = ""
        if obj.diagnosi_type == diagnositypes.DISEASE:
            for disease in obj.disease.all():
                _diagnosi += f"<div class='row'> - {disease.name}</div>"
        elif obj.diagnosi_type == diagnositypes.INJURY:
            for injury in obj.injury.all():
                _diagnosi += f"<div class='row'> - {injury.name}</div>"
        return format_html(_diagnosi)
        
    @display(description='المستشفى')
    def _hospital(self,obj):
        return obj.hospital.name
    @display(description='الإجراءات الطبية')
    def _procedure(self,obj):
        procedures = ''
        for pro in obj.procedure.all():
           procedures += f"<div class='row'>- {pro.name}</div>"
        return format_html(procedures)
    @display(description='النتيجة')
    def _result(self,obj):
        result = None
        for key,value in self.model.Results.choices:
            print(key,value)
            if key == obj.result:
                result = value
        return result or "-"
        
    


    @display(description='نوع الدخول')
    def _entry_type(self,obj):
        return obj.entry_type
    @display(description='أسباب الإصابة')
    def _because_injury(self,obj):
        bec = ''
        for be in obj.becauseinjury.all():
           bec += be.name + ' و'
        return bec[:-1]
   
    
    @display(description='رقم البلاغ')
    def _number_notification(self,obj):
        if obj.entry_type == 'دخول جديد':
            return "obj.number_notification"
        elif obj.entry_type == 'عودة':
            return "obj.back.number_notification"
        else:
            return ''
    @display(description='التاريخ')
    def _date(self,obj):
        return utils.date_format(obj.datetime.date())
    
    def get_list_display(self, request):
        list_display=["_date",
            '_profilemedical_name','_profilemedical_name_2',
            "_profilemedical_supervisor_general","_profilemedical_supervisor_direct",
            "diagnosi",'_hospital','_procedure',"_result",
        
        ]
        return list_display
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        w = models.Entry.objects.filter(type_entry="عودة")
        ex = {}
        for i in w:
            ex["id"] = i.back.id
        print(ex)
        if db_field.name == 'back':
            kwargs['queryset'] = models.Entry.objects.filter(result="عودة").exclude(**ex)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_urls(self):
        my_urls = [
            path("change_form_chek_api/",self.admin_site.admin_view(self.change_form_chek_api),name="entry_change_form_chek_api"),
        ]
        return my_urls + super().get_urls()
    
    def change_form_chek_api(self,request):
        entry = models.Entry
        data = json.loads(request.body)
        fields = data["fields"] or {}
        print(fields)
        res_fields = []
        fields["back"]["hidden"] = True
        fields["number_notification"]["hidden"] = True
        fields["diagnosi_type"]["hidden"] = True
        fields["injury"]["hidden"] = True
        fields["disease"]["hidden"] = True
        fields["becauseinjury"]["hidden"] = True

        
        fields["period_digg"]["hidden"] = True
        fields["hospital_turn"]["hidden"] = True
        fields["date_back"]["hidden"] = True
        fields["report_death"]["hidden"] = True
        


        if fields["entry_type"]["value"] == entry.EntryTypes.NEW:
            fields["number_notification"]["hidden"] = False
            fields["diagnosi_type"]["hidden"] = False

            fields["back"]["value"] = ''


            if fields["diagnosi_type"]["value"] == entry.DiagnosiTypes.DISEASE:
                fields["disease"]["hidden"] = False

                fields["injury"]["value"] = ''
                fields["becauseinjury"]["value"] = ''

            elif fields["diagnosi_type"]["value"] == entry.DiagnosiTypes.INJURY:
                fields["injury"]["hidden"] = False
                fields["becauseinjury"]["hidden"] = False

                fields["disease"]["value"] = ''

        elif fields["entry_type"]["value"] == entry.EntryTypes.BACK:
            fields["back"]["hidden"] = False

            fields["number_notification"]["value"] = ''
            fields["diagnosi_type"]["value"] = ''

        
        if fields["result"]["value"] == entry.Results.DIGG:
            fields["period_digg"]["hidden"] = False

            fields["hospital_turn"]["value"] = ''
            fields["date_back"]["value"] = ''
            fields["report_death"]["value"] = ''


        if fields["result"]["value"] == entry.Results.TURN:
            fields["hospital_turn"]["hidden"] = False

            fields["period_digg"]["value"] = ''
            fields["date_back"]["value"] = ''
            fields["report_death"]["value"] = ''

        if fields["result"]["value"] == entry.Results.BACK:
            fields["date_back"]["hidden"] = False

            fields["period_digg"]["value"] = ''
            fields["hospital_turn"]["value"] = ''
            fields["report_death"]["value"] = ''

        if fields["result"]["value"] == entry.Results.DEATH:
            fields["report_death"]["hidden"] = False

            fields["period_digg"]["value"] = ''
            fields["hospital_turn"]["value"] = ''
            fields["date_back"]["value"] = ''
        

        for name,field in fields.items():
            if "value" in field:
                res_fields += [{
                    "name":name,
                    'value':field["value"],
                    "hidden":field["hidden"],
                }]


        print(fields)
        return JsonResponse(data={"fields":res_fields})

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(
            change_form_chek_api_url = reverse("admin:entry_change_form_chek_api")
        )
        return super().changeform_view(request, object_id, form_url, extra_context)
    
