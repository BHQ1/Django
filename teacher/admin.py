from django.contrib import admin
from teacher.models import Teacher
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class TeacherAdmin(admin.ModelAdmin):
    #配置展示列表
    list_display = ('name','email','class_name','gender','phone')
    #配置过滤查询字段
    list_filter = ('class_name','name')
    #配置可以搜索的字段
    search_fields = (['class_name','name'])
    #定义后台列表显示每页的数量
    list_per_page = 30
    #定义列表显示的顺序，负号为降序
    ordering = ('-created_at',)

    #显示字段
    fieldsets = (
        (None,{
            'fields':('name','email','class_name','gender','phone')
        }),
    )

    def save_model(self, request, obj, form, change):
        user = User.objects.create(
            email=request.POST.get('email'), #获取邮箱
            username= request.POST.get('email'), #使用email作为用户登录名
            password=make_password(settings.TEACHRE_INIT_PASSWORD), #密码加密
            is_staff= 1  #允许作为管理员登录后台
        )
        obj.tid=obj.user_id=user.id #获取新增用户id，作为tid和user_id
        super().save_model(request,obj,form,change)
        return

    def delete_queryset(self, request, queryset):
        #删除多条记录，提示删除user表中信息
        for obj in queryset:
            obj.user.delete()
        super().delete_model(request,obj)
        return

    def delete_model(self, request, obj):
        #删除单挑记录，提示删除user表中数据
        super().delete_model(request,obj)
        if obj.user:
            obj.user.delete()
        return

#设置后台页面头部显示内容和页面标题
admin.site.site_header = '智慧星学生管理系统'
admin.site.site_title = '智慧星学生管理系统'
#绑定模型到管理后台
admin.site.register(Teacher,TeacherAdmin)