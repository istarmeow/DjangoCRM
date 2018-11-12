from django.urls import path
from djadmin.views import index, user_login, user_logout, table_detail

app_name = 'djadmin'

urlpatterns = [
    path('login/', user_login, name='user_login'),  # djAdmin登录
    path('logout/', user_logout, name='user_logout'),  # djAdmin登出
    path('', index, name='index'),  # djAdmin主页
    path('<str:app_name>/<str:model_name>/', table_detail, name='table_detail'),  # 数据表详情
]
