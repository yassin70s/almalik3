from typing import Any
from main.view import *
from . import models


class Site(Site):
    def each_context(self, request):
        return {
            "notice_change_list_api_url":reverse(f"api:almalik_noticeuser_changelist"),
            **super().each_context(request)
        }
    def login(self, request, extra_context = None):
        extra_context = extra_context or {}

        is_login = False
        is_soon = True
        is_knowledge = True




        extra_context.update(
            is_login = is_login,
            is_soon = is_soon,
            is_knowledge = is_knowledge,
            

        )
        return super().login(request, extra_context)

site = Site(name="view")






class ChatView(ModelView):
    def changelist_view(self, request, extra_context=None):
        extra_context = {
            "change_list_usercontact_api_url":reverse(f"api:{self.opts.app_label}_usercontact_changelist"),
            "add_api_url":reverse(f"api:{self.opts.app_label}_chat_add"),
        }
        print(555)
        return super().changelist_view(request, extra_context)
