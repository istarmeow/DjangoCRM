from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout


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
            return redirect(reverse('crm:index'))
        login_msg = '用户名或密码错误！'
    return render(request, 'login.html', locals())


def user_logout(request):
    logout(request)
    return redirect(reverse('user_login'))