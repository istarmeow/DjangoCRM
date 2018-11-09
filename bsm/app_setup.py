from django import conf


def bsm_auto_discover():
    for app_name in conf.settings.INSTALLED_APPS:
        try:
            # 去每个app下执行bsm.py文件
            # crm.apps.CrmConfig和crm需要做判定
            mod = __import__('{}.admin_bsm'.format(app_name if not 'Config' in app_name else app_name.split('.')[0]))
            # 打印每个app已注册的model名字
            print(mod.admin_bsm)
            # 会打印：<module 'crm.bsm' from 'E:\\Sync\\OneDrive\\PycharmProjects\\DjangoCRM\\crm\\bsm.py'>
        except ImportError:
            pass
