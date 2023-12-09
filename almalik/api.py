from main.api import *
from . import admin, models
from django.contrib.auth import models as auth_models
import json
from django.http.response import JsonResponse
class Site(Site):
    def register_user(self,request):
        data = json.loads(request.body).get("data")
        print(data)
        print(data)
        errors = {}
        errors_count = 0
        if not "first_name" in data :
            errors["first_name"] = ["الاسم الاول مطلوب"]
            errors_count += 1
        if not "last_name" in data :
            errors["last_name"] = ["الاسم الاخير مطلوب"]
            errors_count += 1
        if not "number_phone" in data:
            errors["number_phone"] = ["رقم الهاتف مطلوب"]
            errors_count += 1
        if not "password_register" in data:
            errors["password_register"] = ["ادخل كلمة السر"]
            errors_count += 1

        if errors_count == 0:
            number_phone = data["number_phone"]
            password_register = data["password_register"]
            if len(number_phone) == 9 and number_phone[0] == "7":
                if number_phone[1] == "7" or number_phone[1] == '8' or number_phone[1] == "3" or number_phone[1] == "1" or number_phone[1] == "0":
                    pass
                else:
                    errors["number_phone"] = ["رقم الهاتف غير صحيح"]
                    errors_count += 1
            else:
                errors["number_phone"] = ["رقم الهاتف غير صحيح"]
                errors_count += 1
            if auth_models.User.objects.filter(username=number_phone).exists():
                errors["number_phone"] = ["رقم الهاتف موجود من قبل"]
                errors_count += 1
            elif not len(password_register) >=7:
                errors["password_register"] = ["يجب أن تكون كلمة المرور 7 محارف على الأقل"]
                errors_count += 1
        if errors_count == 0:
            """print(errors_count,number_phone,auth_models.User.objects.filter(username=number_phone).exists())
            model_user = models.User()
            model_user.username = number_phone
            model_user.password = data["password_register"]
            model_user.first_name=data["first_name"]
            model_user.last_name = data["last_name"]
            model_user.is_active = True
            model_user.is_staff = True
            model_user.save()"""
            auth_models.User.objects.create_user(
                username = number_phone,
                password=data["password_register"],
                first_name=data["first_name"],
                last_name = data["last_name"],

                is_active = True,
                is_staff = True,

            ).groups.add(auth_models.Group.objects.get(name="almalik_users"))
            user = auth_models.User.objects.get(username=number_phone)
            models.UserContact.objects.update_or_create(
                user = user,
                contact = auth_models.User.objects.get(username="almalik"),
            )
            models.UserContact.objects.update_or_create(
                    user = auth_models.User.objects.get(username="almalik"),
                    contact = user,
            )
            models.Balance.objects.update_or_create(
                user = user,
                balance_type = models.BlanceType.objects.get_or_create(name="$")[0],
            )
            models.Profile.objects.update_or_create(
                    user = user,
            )
            models.Setting.objects.update_or_create(
                user = user,
            )
            
            return JsonResponse(data={"data":data})
        else:
            errors_content = ""
            for key,value in errors.items():
                errors_content += f"<div class='row'> - {value[0]}</div>"
            return JsonResponse(data={"errors":errors,"detail":errors_content})

site = Site(name = "api")




class BalanceApi(ModelApi,admin.BalanceAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(user=request.user)



class BalanceReceiveApi(ModelApi,admin.BalanceReceiveAdmin):
    fields = ["receive_type","number","amount"]

    def log_addition(self, request, object, message):
        object.user = request.user
        object.balance = models.Balance.objects.get(user=request.user)
        object.save()
        models.NoticeUser.objects.create(
            notice= models.Notice.objects.create(
                content = "تم استلام الطلب"
            ),
            user = object.user,
        )
        return super().log_addition(request, object, message)

class ProjectApi(ModelApi,admin.ProjectAdmin):
    list_display = ["id","department","title","datetime_add","_statu","project_offers"]
    fields = ["department","name","price_min","price_max","days",]
    
    
    inlines = []
 
    def log_addition(self, request, object, message):
        print(object.id,7654)
        object.user = request.user
        object.save()

        return super().log_addition(request, object, message)

class UserContactApi(ModelApi,admin.UserContactAdmin):
    list_display = ["userId","name","path","time","preview","messages","active"]

    def userId(self,obj):
        return obj.contact.id
    def name(self,obj):
        return obj.contact.first_name
    def path(self,obj):
        return "logo.png"
    def time(self,obj):
        return datetime.now().time()
    def preview(self,obj):
        return ""
    def messages(self,obj):
        #qs = models.Chat.objects.filter(user=obj.user).union(models.Chat.objects.filter(to_user=obj.user))
        qss = models.Chat.objects.filter(to_user=obj.user).filter(user=obj.contact)
        qsss = models.Chat.objects.filter(user=obj.user).filter(to_user=obj.contact)
        qs = qss.union(qsss)
        #me_time = co.datetime_add.time()
        return [{"fromUserId":co.user.id,"toUserId":co.to_user.id,"text":co.text,"time":co.datetime_add.date() } for co in qs]
    def active(self,obj):
        return True
    
    def get_queryset(self, request):
        #if not request.user.is_superuser:
        return super().get_queryset(request).filter(user=request.user)
        #return super().get_queryset(request)

class NoticeUserApi(ModelApi):
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
        queryset = super().get_queryset(request)
        if not request.user.username == "yassin":
            queryset = queryset.filter(user=request.user)
        if queryset.filter(is_view = False).exists():
            queryset.filter(is_notice = True,is_view=False).update(is_view = True)
            queryset.filter(is_notice=False).update(is_notice=True)
            
        return queryset
    def changelist_view(self, request, **kwargs):
        
        return super().changelist_view(request, **kwargs)
    