from djadmin.sites import site
from crm import models
from djadmin.djadmin_base import BaseDjAdmin

print('crm models...')


# 注册model
class CustomerInfoAdmin(BaseDjAdmin):  # 不使用object，直接继承BaseDjAdmin
    list_display = ['name', 'contact_type', 'contact', 'consultant', 'consult_content', 'status', 'created_time']
    list_filter = ['source', 'consultant', 'status', 'created_time']
    search_fields = ['contact', 'consultant__name']


site.register(models.CustomerInfo, CustomerInfoAdmin)

site.register(models.Role)
site.register(models.Menu)
site.register(models.UserProfile)