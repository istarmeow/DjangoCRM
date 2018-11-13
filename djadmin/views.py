from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
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
        # 分页将不计入筛选值
        if k == 'page' or k.startswith('_'):
            continue
        if v:  # 所选的值不会空是保存到字典中
            filter_conditions[k] = v
    return queryset.filter(**filter_conditions), filter_conditions


def get_order_result(request, queryset, admin_class):
    """获取request中的排序字段，然后返回排序后的结果"""
    current_order_field = dict()
    # 通过获取前端传过来的排序的索引字符串
    order_value = request.GET.get('_order')  # _order的值为list_display列表的索引：-0, 0, 1, -3等
    if order_value:
        # 通过索引找到要排序的字段，因为索引可能是正数或负数，所以要用绝对值
        order_field = admin_class.list_display[abs(int(order_value))]
        # 记录当前的排序字段，以list_display列表的值为键，request的值为值保存到字典中
        current_order_field[order_field] = order_value
        # 判断是正序或者是倒序，如果是倒序，需要添加负号
        if order_value.startswith('-'):
            order_field = '-' + order_field
        return queryset.order_by(order_field), current_order_field
    else:
        return queryset, current_order_field


def get_search_result(request, queryset, admin_class):
    """搜索"""
    keyword = request.GET.get('_kw', '')
    if keyword:
        from django.db.models import Q
        q = Q()
        q.connector = 'OR'

        for search_field in admin_class.search_fields:
            q.children.append(("{}__contains".format(search_field), keyword))
        # print(q)  # (OR: contact__contains, consultant__name__contains)
        queryset = queryset.filter(q)
    return queryset, keyword


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

    # 搜索
    queryset, keyword = get_search_result(request, queryset, admin_class)
    admin_class.search_keyword = keyword  # 将搜索字符串保存到全局类中

    # 排序，返回排序的结果和排序的字段字典
    queryset, current_order_field = get_order_result(request, queryset, admin_class)
    # print(current_order_field)  # {'consult_content': '4'}
    # 如果有排序，保存排序的值，用于模板中在分页模块显示
    if current_order_field.values():
        current_order_value = list(current_order_field.values())[0]
    else:
        current_order_value = ''

    # 查询集结果分页
    paginator = Paginator(queryset, 10)  # Show 10 contacts per page
    page = request.GET.get('page')
    try:
        queryset = paginator.get_page(page)
    except PageNotAnInteger:
        queryset = paginator.get_page(1)
    except EmptyPage:
        queryset = paginator.get_page(paginator.num_pages)

    return render(request, 'djadmin/table_detail.html', locals())