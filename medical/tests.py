from django.test import TestCase

# Create your tests here.


from . import models,models_old
print(5656)

"""def create_object(model,object,fields={},defaults={}):
    obj = {}
    id = None
    for field in model._meta.get_fields():
        field_name = field.name
        field_value = None
        in_field = None
        id = object.id
        if not field.one_to_many:
            if field_name in fields and hasattr(object,fields[field_name]):
                in_field = fields[field_name]
            elif hasattr(object,field_name):
                in_field = field_name

            
            if field_name in defaults:
                field_value = defaults[field_name]
            elif in_field and not getattr(object,in_field) == None:
                if field.many_to_one:
                    print(field.many_to_one,8787)
                    fk_object = getattr(object,in_field)
                    related_model = field.related_model
                        #if not related_model.objects.filter(id=fk_object.id).exists():
                            #create_object(related_model,fk_object,fields,defaults)
                    field_value = related_model.objects.get(id=fk_object.id)
                                #field.related_model.objects.filter(id=object.id).update_or_create(create_object(field.related_model,object))
                elif field.many_to_many:
                    print(field.many_to_one,6)
                    related_model = field.related_model
                    fk_objects = getattr(object,in_field)
                    field_value = related_model.objects.all()
                    #field_value = getattr(object,in_field).all()
                else:
                    
                    field_value = getattr(object,in_field)


            obj[field_name] = field_value
            
    print(obj)

    #obj["id"] = None
    if not model.objects.filter(id=id).exists():
        model.objects.create(
            **obj
        )

        
"""
    
    
   

import time




def dd():
    for model_list,fields,defaults in [
        ((models.Hospital,),{},{}),
        ((models.Axi,),{},{}),
        ((models.Unit,),{},{}),
        ((models.SupervisorGeneral,),{},{}),
        ((models.SupervisorDirect,),{"supervisor_general_id":None},{}),


        ((models.Province,),{},{}),

        ((models.CategoreDisease,),{},{}),

        ((models.CategoreInjury,),{},{}),

        ((models.CategoreProcedure,),{},{}),
        ((models.CategoreBecauseInjury,),{},{}),

        ((models.Directorate,),{},{}),
        ((models.Area,),{},{}),
        ((models.Disease,),{},{}),

        ((models.Injury,),{},{}),
        ((models.Procedure,),{},{}),
        ((models.BecauseInjury,),{},{}),

        ((models.ProfileMedical,models_old.File),{
            "supervisor_general_id":models_old.SupervisorGeneral,
            "supervisor_direct_id":models_old.SupervisorDirect,
            "unit_id":models_old.Unit,
            },
            {"axi_id":models.Axi.objects.get_or_create(name="محور")[0].pk,
            "supervisor_general_id":models.SupervisorGeneral.objects.first().id,
            "supervisor_direct_id":models.SupervisorDirect.objects.first().id,
            "unit_id":models.Unit.objects.first().id,
             
             
             }),
        #((models.Entry,),{"datetime":"date","profilemedical":"fiel"},{}),
        

        ]:
        model = model_list[0]
        model_old = None
        #model.objects.all().delete()
        if len(model_list) == 2 :
            model_old = model_list[1]
        elif hasattr(models_old,model._meta.object_name):
            model_old = getattr(models_old,model._meta.object_name)
        if model_old:
            for qs in model_old.objects.values():
                qs = qs or {}
                for key,value in fields.items():
                    if key in qs:
                        if value == None:
                            qs.pop(key)
                        elif hasattr(value,"_meta"):
                            #qs[key] = getattr(models,value._meta.object_name).objects.get(name=value.objects.get(id=key).name).id
                            print(656565)
                for key,value in defaults.items():
                    qs[key] = value
                if hasattr(model,"is_group") and model.is_group == True:
                    qs.pop("id")
                    print(qs,model)

                model.objects.update_or_create(
                    **qs
                )

        #time.sleep(3)    


#dd()    
#models.User.objects.all().delete()

model_entry = models.Entry

def ss():
    for entry in models_old.Entry.objects.all():
        entry_type = None
        back = None
        diagnosi_type = None
        injury = None
        disease = None
        becauseinjury = None
        becauseinjury = None
        result = None
        recipe = None

        hospital_turn = None
        date_back = None
        if entry.type_entry == "دخول جديد":
            entry_type = model_entry.EntryTypes.NEW
        elif entry.type_entry == "عودة":
            entry_type = model_entry.EntryTypes.BACK
        


        if not entry.back == None:
            back = models.Entry.objects.get(id=entry.back.id)

        if entry.type_diagnosi == "مريض":
            diagnosi_type = model_entry.DiagnosiTypes.DISEASE
        elif entry.type_diagnosi == "جريح":
            diagnosi_type = model_entry.DiagnosiTypes.INJURY
        elif entry.type_diagnosi == "شهيد":
            diagnosi_type = model_entry.DiagnosiTypes.DEATH
        
        if entry.result == "معالجة":
            result = model_entry.Results.TREATMENT
        elif entry.result == "رقود":
            result = model_entry.Results.DIGG
        elif entry.result == "عودة":
            result = model_entry.Results.BACK
        elif entry.result == "وفاة":
            result = model_entry.Results.DEATH
        elif entry.result == "تحويل":
            result = model_entry.Results.TURN
        
        if not entry.hospital_turn == None:
            hospital_turn = models.Hospital.objects.get(name=entry.hospital_turn.name),
        entry_new = models.Entry.objects.filter(id=entry.id)
        if not entry_new.exists():
            entry_new.create(id=entry.id)
        else:
            entry_new.update(
                hospital = models.Hospital.objects.get(name=entry.hospital.name),
                profilemedical = models.ProfileMedical.objects.get(name=entry.fiel.name),
                datetime = entry.date,
                entry_type = entry_type,
                back = back,
                number_notification = entry.number_notification,
                diagnosi_type = diagnosi_type,
                #injury = injury,
                #disease = disease,
                #becauseinjury = becauseinjury,
                #procedure = becauseinjury,
                result = result,
                recipe = recipe,
                period_digg = entry.period_digg,
                #hospital_turn = hospital_turn,
                date_back = entry.date_back,
                report_death = entry.report_death,
            )
        print(22,entry)
        
        entry_new = entry_new.first()
        if entry.injury:
            print(entry.injury,9898)
            """entry_new.injury.set(
                models.Injury.objects.filter(id__in = [id.id for id in entry.injury.all()]).all()
            )"""
        """if not entry.disease == None:
            entry_new.disease.set(
                models.Disease.objects.filter(id__in = [id.id for id in entry.disease.all()])
            )
        if not entry.because_injury == None:
            entry_new.becauseinjury.set(
                models.BecauseInjury.objects.filter(id__in = [id.id for id in entry.because_injury.all()])
            )
        if not entry.procedure == None:
            entry_new.procedure.set(
                models.Procedure.objects.filter(id__in = [id.id for id in entry.procedure.all()])
            )"""
        print(entry_new)
#Sss()
#models.Entry.objects.all().delete()