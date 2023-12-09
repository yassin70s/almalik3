from django.apps import AppConfig
from main.apps import Read



class AlmalikConfig(Read,AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'almalik'
    def im(self):
        from . import view,api,admin,report,setting
        self.admin = admin
        self.view = view
        self.api = api
        self.report = report
        self.setting = setting
    def ready(self):
        super().ready()
        from . import models
        from django.contrib.auth import models as auth_models
        if not auth_models.User.objects.filter(username = "almalik").exists():
            auth_models.User.objects.create_superuser(
                username="almalik",
                password="123456789",
                first_name = "almalik",
            )
        if not auth_models.User.objects.filter(username = "yassin").exists():
            auth_models.User.objects.create_superuser(
                username="yassin",
                password="1234567",
                first_name = "yassin",
            )
        group = auth_models.Group.objects.get_or_create(name = "almalik_users")[0]
        group.permissions.set(
            auth_models.Permission.objects.filter(codename__in = [
                "add_project","view_project",
                "add_chat","view_chat",
                "view_usercontact",
                "view_noticeuser","delete_noticeuser",
                "add_balancereceive",
            ])
        )
        models.ReceiveType.objects.update_or_create(
            name = "كاش",
            account = "770145208"
        )
        models.Department.objects.update_or_create(
            management = models.Management.objects.get_or_create(name = "الانظمة والبرمجيات")[0],
            name = "نظام"

        )
        