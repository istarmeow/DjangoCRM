from django.template import Library
from django.utils.safestring import mark_safe


register = Library()


# 显示模型表的中文名称
@register.simple_tag
def build_table_head_name(admin_class):
    th = ''
    for display_field in admin_class.list_display:
        # 获取列中的字段对象
        display_field_obj = admin_class.model._meta.get_field(display_field)
        # print(display_field_obj.verbose_name)
        tmp = "<th>{}</th>".format(display_field_obj.verbose_name)
        th += tmp
    return mark_safe(th)


# 显示表数据
@register.simple_tag
def build_table_body(obj, admin_class):
    """
    生成一条记录的html元素
    :param obj: 一个模型查询集中的一个对象
    :param admin_class: 自定义注册的类
    :return: 得到这个对象要求显示的所有列
    """
    td = ''
    for display_field in admin_class.list_display:
        # 获取列中的字段对象
        display_field_obj = admin_class.model._meta.get_field(display_field)
        # print(display_field_obj)
        # 字段对象choices方法，如果有choices，则使用get_xxx_display
        if display_field_obj.choices:
            # print('get_{}_display'.format(display_field))
            display_field_data = getattr(obj, 'get_{}_display'.format(display_field))()  # 使用get_xxx_display()需要带括号，调用函数执行结果，而不带括号得到的是函数对象
        else:
            # 根据属性名，获取对象的属性值，两个参数，一个对象obj，一个列名
            display_field_data = getattr(obj, display_field)  # 获取一个对象的属性值，例如<CustomerInfo: 小东>对象，得到他的name属性，值为小东
        tmp = "<td>{}</td>".format(display_field_data)
        td += tmp
    return mark_safe(td)


@register.simple_tag
def build_option_filter(filter_field, admin_class):
    select = "<select name='{}' class='form-control'>".format(filter_field)
    # 获取列中的字段对象
    filter_field_obj = admin_class.model._meta.get_field(filter_field)
    try:
        for choice in filter_field_obj.get_choices():  # choice[0]为选项的值，choice[1]为选中的可见内容
            # 获取过滤字典中的值，并在模板中呈选中状态
            selected = ''
            if filter_field in admin_class.filter_conditions:
                # 如果当前值被选中
                if str(choice[0]) == admin_class.filter_conditions.get(filter_field):
                    selected = 'selected'

            option = "<option value='{}' {}>{}</option>".format(choice[0], selected, choice[1])
            select += option
    except AttributeError as e:
        # 对时间使用单独的select
        select = "<select  class='form-control' name='{}__gte'>".format(filter_field)
        # print(filter_field_obj.get_internal_type())  # 这儿得到的结果是：DateField
        if filter_field_obj.get_internal_type() in ('DateField', 'DateTimeField'):
            import datetime
            now_time = datetime.datetime.now()
            filter_time_list = [
                ('', '所有时间'),
                (now_time, '今天'),
                (now_time - datetime.timedelta(7), '7天内'),  # 往前7天
                (now_time.replace(day=1), '本月'),  # 本月内
                (now_time - datetime.timedelta(90), '三个月内'),
                (now_time.replace(month=1, day=1), '本年'),
            ]
            for dt in filter_time_list:
                # 如果选择的时间值不为空，则进行时间格式化
                time_to_str = '' if not dt[0] else dt[0].strftime('%Y-%m-%d')  # 需要将时间格式化成：YYYY-MM-DD
                # 修改name后，过滤时间的参数变成了created_time__gte=2018-11-03，所以下方的选中，需要进行修改

                # 设置选中
                selected = ''
                if filter_field + '__gte' in admin_class.filter_conditions:
                    # 如果当前值被选中
                    if time_to_str == admin_class.filter_conditions.get(filter_field + '__gte'):
                        selected = 'selected'

                option = "<option value='{}' {}>{}</option>".format(time_to_str, selected, dt[1])
                select += option
    select += "</select>"
    return mark_safe(select)
