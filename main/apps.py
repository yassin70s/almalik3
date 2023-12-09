from django.apps import AppConfig

class Read:
    def im(self):
        from . import view,api,admin,report,setting
        self.admin = admin
        self.view = view
        self.api = api
        self.report = report
        self.setting = setting
    def ready(self):
        self.im()
        super().ready()
        
        
       
        for model in self.models.values():
            for module_name, module in  [("view",self.view),("api",self.api),("admin",self.admin),("report",self.report),("setting",self.setting)]:
                setattr(module,"ee",9)
                if hasattr(model,f"is_{module_name}"):
                    has_module = getattr(model,f"is_{module_name}")
                    if has_module == True:
                        if hasattr(module,"site"):
                            
                            site = getattr(module,"site")
                            admin_class = None
                            if hasattr(module,f"{model._meta.object_name}{site.name.capitalize()}"):
                                admin_class = getattr(module,f"{model._meta.object_name}{site.name.capitalize()}")
                            elif hasattr(module,f"Model{site.name.capitalize()}"):
                                admin_class = getattr(module,f"Model{site.name.capitalize()}")
                                if not site.name == "admin" and hasattr(self.admin,f"{model._meta.object_name}Admin"):
                                    admin_class = type(f"{model._meta.object_name}{site.name.capitalize()}",(
                                        getattr(module,f"Model{site.name.capitalize()}"),
                                        getattr(self.admin,f"{model._meta.object_name}Admin")
                                        ),
                                        {},
                                        )
                                
                            
                            
                            site.register(model,admin_class)
                
            if hasattr(model,"is_group"):
                has_group = getattr(model,"is_group")
                if has_group == True:
                    model().create_group_model()
                    
                    
        


class MainConfig(Read,AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'



