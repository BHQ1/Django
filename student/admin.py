from django.contrib import admin
from student.models import Student
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class StudentAdmin(admin.ModelAdmin):
    #配置展示列表
    list_display = ('student_num','name','class_name',
                    'teacher_name','gender','birthday')
    #配置过滤，查询字段
    list_filter = ('name','student_num')
    #配置搜索字段
    search_fields = (['name','student_num'])
    readonly_fields = ('teacher',) #设置只读字段，不可以更改
    ordering = ('-created_at',) #定义列表显示顺序
    fieldsets = (
        (None, {
            'fields': ('student_num', 'name', 'gender', 'phone', 'birthday')
        }),
    )

    def save_model(self, request, obj, form, change):
        #添加student表时，同时添加到user表
        #因为需要和tracher表级联，所以自动获取当前登录的老师id作为teacher_id
        if not change:
            user = User.objects.create(
                username=request.POST.get('student_num'), #使用学号登录
                password=make_password(settings.STUDENT_INIT_PASSWORD)
            )
            obj.user_id = user.id #获取新增用户的id
            obj.teacher_id = request.user.id #获取当前老师的id
            super().save_model(request,obj,form,change) #调用父类保存方法
            return

    def delete_queryset(self, request, queryset):
        #删除多条记录，同时删除user表中数据
        for obj in queryset:
            obj.user.delete()
        super().delete_model(request,obj)
        return
    def delete_model(self, request, obj):
        #删除单挑记录，同时删除user表中记录
        super().delete_model(request,obj)
        if obj.user:
            obj.user.delete
        return

#绑定到管理后台
admin.site.register(Student,StudentAdmin)