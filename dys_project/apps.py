from  django.contrib.admin.apps import AdminConfig


# Override default admin site
class MyAdminConfig(AdminConfig):
    default_site = "dys_project.admin.MyAdminSite"
    