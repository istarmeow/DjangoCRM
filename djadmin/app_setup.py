from django import conf


def djadmin_auto_discover():
    for app_name in conf.settings.INSTALLED_APPS:
        try:
            # 去每个app下执行djadmin.py文件
            # crm.apps.CrmConfig和crm需要做判定
            mod = __import__('{}.djadmin'.format(app_name if 'Config' not in app_name else app_name.split('.')[0]))
            # 打印每个app已注册的model名字
            print(mod.djadmin)
            # 会打印：<module 'crm.djadmin' from 'E:\\Sync\\OneDrive\\PycharmProjects\\DjangoCRM\\crm\\djadmin.py'>
        except ImportError:
            pass