from django.apps import AppConfig
from main.apps import Read



class AppConfig(Read,AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    def im(self):
        from . import view,api,admin,report,setting
        self.admin = admin
        self.view = view
        self.api = api
        self.report = report
        self.setting = setting
    def ready(self):
        return super().ready()
    
    