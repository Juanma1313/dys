from django.contrib import admin
from django.utils.http import urlencode

class MyAdminSite(admin.AdminSite):
    '''Overrides the default admin site to enable default filter options'''
    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request)
        for app_dict in app_list:
            for model_dict in app_dict["models"]:
                #print(f"model_dict={model_dict}")
                obj_name = model_dict["object_name"]
                model_admin=None
                for reg_model, instance in self._registry.items():
                    model_class=str(reg_model)
                    if "."+obj_name in model_class:    # Search the matching registered model 
                        model_admin = instance
                        #print(f"{obj_name} found in {model_class}")
                    #else:
                    #    print(f"{obj_name} not in {model_class}")
                if model_admin is not None:
                    if default_filters := getattr(model_admin, "default_list_filters", None):
                        org_url=model_dict['admin_url']
                        model_dict['admin_url'] += '?' + urlencode(default_filters)
                        print(f"Changed url from {org_url} to {model_dict['admin_url']}")

        #for app in app_list:
        #    print(f"app={app['name']}")
        #    for model in app['models']:
        #        print(f"model={model}")

        #for cls, inst in self._registry.items():
        #    print(f"class={cls},  cls.__class__={cls.__class__}")
        return app_list