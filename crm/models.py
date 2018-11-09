from django.db import models
from django.contrib.auth.models import User


class Menu(models.Model):
    """动态菜单"""
    Url_Type_Choices = (
        (0, '绝对URL'),
        (1, '动态URL')
    )
    name = models.CharField(max_length=100, verbose_name='菜单名称')
    url_type = models.SmallIntegerField(choices=Url_Type_Choices, default=0, verbose_name='菜单类型')
    url = models.CharField(max_length=200, verbose_name='URL地址')

    class Meta:
        unique_together = ('name', 'url')
        verbose_name_plural = verbose_name = '动态菜单'

    def __str__(self):
        return self.name


class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=50, unique=True, verbose_name='角色名称')
    menus = models.ManyToManyField(Menu, blank=True, verbose_name='动态菜单')  # 一个角色可以访问多个菜单，一个菜单可以被多个角色访问

    class Meta:
        verbose_name_plural = verbose_name = '角色'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """用户信息表"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile', verbose_name='关联系统User')  # 扩展user模型
    name = models.CharField(max_length=50, verbose_name='姓名')
    role = models.ManyToManyField(Role, related_name='userprofile', verbose_name='角色列表')

    class Meta:
        verbose_name_plural = verbose_name = '用户'

    def __str__(self):
        return self.name


class Branch(models.Model):
    """校区分支"""
    name = models.CharField(max_length=50, unique=True, verbose_name='校区名')
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name='地址')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '校区'


class Course(models.Model):
    """课程表"""
    name = models.CharField(max_length=50, unique=True, verbose_name='课程名称')
    price = models.PositiveSmallIntegerField(verbose_name='价格')  # 整数
    period = models.PositiveSmallIntegerField(verbose_name='课程周期（月）', default=5)
    outline = models.TextField(verbose_name='大纲')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '课程'


class Class(models.Model):
    """班级信息"""
    Class_Type_Choices = (
        (1, '工作日'),
        (2, '周末'),
        (3, '网络班')
    )
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, verbose_name='所属校区')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    class_type = models.SmallIntegerField(choices=Class_Type_Choices, verbose_name='班级类型')
    semester = models.SmallIntegerField(verbose_name='学期')
    teachers = models.ManyToManyField(UserProfile, verbose_name='讲师')
    start_date = models.DateField(verbose_name='开班日期')
    graduate_date = models.DateField(blank=True, null=True, verbose_name='毕业日期')  # 结束日期不固定，可为空

    class Meta:
        verbose_name_plural = verbose_name = '班级信息'
        unique_together = ('branch', 'course', 'class_type', 'semester')  # 联合唯一，班级不能重复

    def __str__(self):
        return '{}({})期'.format(self.course.name, self.semester)


class CourseRecord(models.Model):
    """上课记录"""
    class_grade = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='班级')
    day_num = models.PositiveSmallIntegerField(verbose_name='课程节次')
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='讲师')
    title = models.CharField(max_length=200, verbose_name='本节主题')
    content = models.TextField(verbose_name='本节内容')
    has_homework = models.BooleanField(default=False, verbose_name='本节是否有作业')
    homework = models.TextField(blank=True, null=True, verbose_name='作业内容')
    created_time = models.DateField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return '{}第({})节'.format(self.class_grade, self.day_num)

    class Meta:
        verbose_name_plural = verbose_name = '上课记录'
        unique_together = ('class_grade', 'day_num')


class CustomerInfo(models.Model):
    """客户信息表"""
    Contact_Type_Choices = (
        (1, 'qq'),
        (2, '微信'),
        (3, '手机'),
        (4, '其他')
    )
    Source_Choice = (
        (1, 'qq群'),
        (2, '微信'),
        (3, '转介绍'),
        (4, '其它'),
    )
    Status_Choice = (
        (1, '未报名'),
        (2, '已报名'),
        (3, '结业')
    )
    name = models.CharField(max_length=50, verbose_name='客户姓名')
    contact_type = models.SmallIntegerField(choices=Contact_Type_Choices, default=1, verbose_name='联系媒介')
    contact = models.CharField(max_length=50, unique=True, verbose_name='联系方式')
    source = models.SmallIntegerField(choices=Source_Choice, verbose_name='客户来源')
    # 如果是转介绍，介绍人是学员，介绍别人来学习，需要关联到学员本人，如果不是，可为空
    referral_from = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='转介绍客户')
    consult_courses = models.ManyToManyField(Course, verbose_name='咨询课程')  # 多对多关联课程
    consult_content = models.TextField(verbose_name='咨询内容')
    status = models.SmallIntegerField(choices=Status_Choice, verbose_name='客户状态')
    consultant = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='课程顾问')
    created_time = models.DateField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '客户信息'


class CustomerFollowUp(models.Model):
    """客户跟进记录"""
    Status_Choices = (
        (0, '近期无报名计划'),
        (1, '一个月内报名'),
        (2, '半个月报名'),
        (3, '已报名')
    )
    customer = models.ForeignKey(CustomerInfo, on_delete=models.CASCADE, verbose_name='客户')
    content = models.TextField(verbose_name='跟进内容')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='跟进人')
    status = models.SmallIntegerField(choices=Status_Choices, verbose_name='客户状态')
    created_time = models.DateField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return "{}跟进{}状态：{}".format(self.user.name, self.customer.name, self.get_status_display())

    class Meta:
        verbose_name_plural = verbose_name = '跟进记录'


class Student(models.Model):
    customer = models.OneToOneField(CustomerInfo, verbose_name='客户', on_delete=models.CASCADE)
    class_grades = models.ManyToManyField(Class, verbose_name='班级')

    class Meta:
        verbose_name_plural = verbose_name = '学员'

    def __str__(self):
        return '{}({})'.format(self.customer, self.class_grades.name)


class StudyRecord(models.Model):
    """学习记录"""
    Score_Choices = (
        (100, 'A+'),
        (90, 'A'),
        (85, 'B+'),
        (80, 'B'),
        (75, 'B-'),
        (70, 'C+'),
        (60, 'C'),
        (40, 'C-'),
        (-50, 'D'),
        (0, 'N/A'),  # not avaliable
        (-100, 'COPY'),  # 抄作业
    )
    Show_Choices = (
        (0, '缺勤'),
        (1, '已签到'),
        (2, '迟到'),
        (3, '早退'),
    )
    course_record = models.ForeignKey(CourseRecord, on_delete=models.CASCADE, verbose_name='课程')
    student = models.ForeignKey(Student, verbose_name='学生', on_delete=models.CASCADE)
    score = models.SmallIntegerField(choices=Score_Choices, default=0, verbose_name='得分')
    show_status = models.SmallIntegerField(choices=Show_Choices, default=1, verbose_name='出勤')
    note = models.TextField(blank=True, null=True, verbose_name='成绩备注')
    created_time = models.DateField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name_plural = verbose_name = '学习记录'

    def __str__(self):
        return '{} {} {}'.format(self.course_record, self.student, self.score)
