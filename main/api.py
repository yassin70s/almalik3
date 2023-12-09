from django_api_admin.options import *
from django_api_admin.sites import *
from django.urls import path
import json
from django.utils.timezone import datetime
from django.http.response import JsonResponse
from . import models
class ModelApi(APIModelAdmin):
    inlines = []

class Site(APIAdminSite,AdminSite):
    
    def get_urls(self):
        
        
        my_urls = [
            path("login/",self.api_admin_view(self.login),name="login"),
            path("register_user/",self.api_admin_view(self.register_user),name="register_user"),
           

        ]
        return my_urls + super().get_urls()
    
    def register_user(self,request):
        data = json.loads(request.body).get("data")
        print(data)
        errors = []
        if not "first_name" in data :
            errors += ["الاسم الاول مطلوب"]
        if not "last_name" in data :
            errors += ["الاسم الاخير مطلوب"]
        if not "number_phone" in data:
            errors += ["رقم الهاتف مطلوب"]
        if not "password_register" in data:
            errors += ["ادخل كلمة السر"]

        if not errors:
            number_phone = data["number_phone"]
            password_register = data["password_register"]
            if models.User.objects.filter(username=number_phone).exists():
                errors += ["رقم الهاتف موجود من قبل"]
            elif not len(password_register) >=7:
                errors += ["يجب أن تكون كلمة المرور 7 محارف على الأقل"]
        
        return JsonResponse(data={"data":data,"errors":errors})
    
#site = Site(name="api")