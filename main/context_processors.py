import os
from django.template import EngineHandler
def get_tempate_name(site_name,app_label,model_name,template_name):
    return ([
        f"{site_name}/{app_label}/{model_name}/{template_name}.html",
        f"{site_name}/{app_label}/{template_name}.html",
        f"{site_name}/{template_name}.html",
        f"{template_name}.html"]
    )

def include_templates(request,site_name,app_label,model_name):
    return {
        "layouts":{
            "auth":get_tempate_name(site_name,app_label,"layouts","auth"),
            "default":get_tempate_name(site_name,app_label,"layouts","default"),
        },
        "common":{
            "footer":get_tempate_name(site_name,app_label,"common","footer"),
            "header":get_tempate_name(site_name,app_label,"common","header"),
            "sidebar":get_tempate_name(site_name,app_label,"common","sidebar"),
            "theme_customiser":get_tempate_name(site_name,app_label,"common","theme_customiser"),
        },
        "model":{
            "change_list":get_tempate_name(site_name,app_label,model_name,"change_list"),
            "change_form":get_tempate_name(site_name,app_label,model_name,"change_form"),
        },

    }
    

            

