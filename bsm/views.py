from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from bsm import app_setup

app_setup.bsm_auto_discover()
from bsm.sites import site

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
            return redirect(reverse('bsm:index'))
        login_msg = '用户名或密码错误！'
    return render(request, 'bsm/login.html', locals())


def user_logout(request):
    logout(request)
    return redirect(reverse('bsm:user_login'))


def index(request):
    return render(request, 'bsm/index.html',
                  {
                      'site': site
                  })
