from django.forms import ModelForm


def create_dynamic_model_form(admin_class):
    """动态生成ModelF"""

    class Meta:
        model = admin_class.model
        fields = '__all__'

    # 通过__new__(cls, *arg, **kwargs)方法，找到ModelForm里面的每个字段，然后循环出每个字段并添加自定义样式
    def __new__(cls, *args, **kwargs):
        # cls.base_fields是一个元组，格式为：OrderedDict([('字段名', 字段的对象), ()])
        # print(cls.base_fields)
        # OrderedDict([('user', <django.forms.models.ModelChoiceField object at 0x000002147D024358>), ('name', <django.forms.fields.CharField object at 0x000002147D0243C8>), ('role', <django.forms.models.ModelMultipleChoiceField object at 0x000002147D0245C0>)])

        for field_name in cls.base_fields:
            # 每个字段的对象
            field_obj = cls.base_fields[field_name]
            # 添加属性
            field_obj.widget.attrs.update({'class': 'form-control'})

        return ModelForm.__new__(cls)

    # 动态生成
    dynamic_form = type('DynamicModelForm', (ModelForm,), {'Meta': Meta, '__new__': __new__})
    return dynamic_form
