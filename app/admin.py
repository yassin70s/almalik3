from main.admin import *


class MyAdmin(ModelAdmin):
    list_display = ["_"]
    def _(self,obj):
        return "_"


