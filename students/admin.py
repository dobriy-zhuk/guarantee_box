from django.contrib import admin
from students.models import (
    Student, StudentStatus, StudentRewardCard,
    Teacher, TeacherStatus, Schedule,
)

admin.site.register(StudentStatus)
admin.site.register(Student)
admin.site.register(TeacherStatus)
admin.site.register(Schedule)
admin.site.register(StudentRewardCard)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    filter_horizontal = ['students']
