from main import admin
class ModelSetting(admin.ModelAdmin):
    pass

class Site(admin.AdminSite):
    pass

site = Site(name="setting")