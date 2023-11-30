from django.contrib import admin
from score.models import Score

class ScoreAdmin(admin.ModelAdmin):
    #配置展示列表
    list_display = ('title','student_num','student','score')
    #配置过滤，查询自段
    list_filter = ('title','student')
    #配置搜索字段
    search_fields = (['title','student_name','student_student_num'])
    ordering = ('-created_at',)
    fieldsets = (
        (None,{
            'fields':('title','student','score')
        }),
    )

#绑定模型到管理后台
admin.site.register(Score,ScoreAdmin)