from django.urls import path
from bsm.views import index, user_login, user_logout

app_name = 'bsm'

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('', index, name='index'),
]
