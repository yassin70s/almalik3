
from typing import Any
from django.contrib.admin import *
from django.core.handlers.wsgi import WSGIRequest
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from . import context_processors
from . import utils

from django.urls import path,reverse
from django.utils.html import format_html
import json
from django.http.response import JsonResponse
from django.utils.timezone import datetime
class ModelAdmin(ModelAdmin):
    
    def changelist_view(self, request, extra_context=None):
        self.change_list_template = None or [
            f"{self.admin_site.name}/{self.opts.app_label}/{self.opts.model_name}/change_list.html",
            f"{self.admin_site.name}/{self.opts.app_label}/change_list.html",
            f"{self.admin_site.name}/change_list.html",
            f"change_list.html",
            f"admin/change_list.html",

        ]
        return super().changelist_view(request, extra_context)
    def changeform_view(self, request, object_id = None, form_url = "", extra_context = None):
        self.change_form_template = None or [
            f"{self.admin_site.name}/{self.opts.app_label}/{self.opts.model_name}/change_form.html",
            f"{self.admin_site.name}/{self.opts.app_label}/change_form.html",
            f"{self.admin_site.name}/change_form.html",
            f"change_form.html",
            f"admin/change_form.html",

        ]
        return super().changeform_view(request, object_id, form_url, extra_context)
    
class AdminSite(AdminSite):
    def __init__(self,name):
        super().__init__(name)
        self.login_template = f"{self.name}/login.html"
    def index(self, request, extra_context = None):
        self.index_template = None or [
            f"{self.name}/index.html",
            f"index.html",
        ]
        return super().index(request, extra_context)
    def app_index(self, request, app_label, extra_context = None):
        self.app_index_template = None or [
            f"{self.name}/{app_label}/app_index.html",
            f"{self.name}/app_index.html",
            f"app_index.html",
            f"admin/app_index.html",

        ]
        return super().app_index(request, app_label, extra_context)

    def login(self, request, extra_context = None):
        return super().login(request, extra_context)
    def logout(self, request, extra_context = None):
        return super().logout(request, extra_context)