from django.contrib import admin
from students.models import (
    Student, StudentStatus, StudentRewardCard,
    Teacher, TeacherStatus, Schedule, FunnelStage
)

admin.site.register(FunnelStage)
admin.site.register(StudentStatus)
admin.site.register(TeacherStatus)
admin.site.register(Schedule)
admin.site.register(StudentRewardCard)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'phone',
        'parent_name', 'parent_phone',
    ]
    readonly_fields = ['age']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    filter_horizontal = ['students']
