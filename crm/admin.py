from django.contrib import admin
from django.apps import apps

# 批量注册models

all_models = apps.get_app_config('crm').get_models()
for model in all_models:
    try:
        admin.site.register(model)
    except:
        pass
