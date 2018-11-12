from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from djadmin import app_setup

app_setup.djadmin_auto_discover()
from djadmin.sites import site

print('site:', site.enable_admins)


def user_login(request):
    login_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        next_url = request.GET.get('next')

        # 验证帐密
        user = authenticate(username=username, password=password)
        if user:
            # 登录并生成session
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect(reverse('djadmin:index'))
        login_msg = '用户名或密码错误！'
    return render(request, 'djadmin/login.html', locals())


def user_logout(request):
    logout(request)
    return redirect(reverse('djadmin:user_login'))


@login_required
def index(request):
    return render(request, 'djadmin/index.html',
                  {
                      'site': site
                  })


def get_filter_result(request, queryset):
    """获取过滤的字段，并返回过滤后的查询集和过滤的字典"""
    filter_conditions = {}
    # 获取过滤的字段
    for k, v in request.GET.items():
        if v:  # 所选的值不会空是保存到字典中
            filter_conditions[k] = v
    return queryset.filter(**filter_conditions), filter_conditions


@login_required
def table_detail(request, app_name, model_name):
    """取出指定model里的数据返回到前端"""
    # 拿到admin_class后，通过它获取model
    admin_class = site.enable_admins[app_name][model_name]
    # print(admin_class)  # 执行djadmin.py定义的注册模型类
    queryset = admin_class.model.objects.all()
    # print(queryset)

    # 进行过滤
    queryset, filter_conditions = get_filter_result(request, queryset)
    # 将过滤字典保存到全局注册类中
    admin_class.filter_conditions = filter_conditions

    return render(request, 'djadmin/table_detail.html', locals())