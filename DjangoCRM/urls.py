"""DjangoCRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import user_login, user_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crm/', include('crm.urls', namespace='crm')),
    path('login/', user_login, name='user_login'),  # 用户登录
    path('logout/', user_logout, name='user_logout'),  # 退出登录
    path('djadmin/', include('djadmin.urls', namespace='djadmin')),  # 后台管理
]

# 上传的文件能直接通过url打开
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
