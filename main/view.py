from typing import Any
from main import admin
from django.urls import reverse
from . import context_processors
class ModelView(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(
            add_api_url=reverse(f"api:{self.opts.app_label}_{self.opts.model_name}_add"),
            add_admin_url=reverse(f"admin:{self.opts.app_label}_{self.opts.model_name}_add",current_app="admin")+"?_popup",
            change_list_api_url=reverse(f"api:{self.opts.app_label}_{self.opts.model_name}_changelist")
        )
        return super().changelist_view(request, extra_context)

class Site(admin.AdminSite):
    def login(self, request, extra_context=None):
        
        


        context = {
            "register_user_url":reverse("api:register_user"),
            "login_api_url":reverse("api:login"),
            "location_url":reverse("admin:index",current_app=self.name),
        }


        extra_context = extra_context or {}
        extra_context.update(context)
        return super().login(request, extra_context)

#site = Site(name="view")