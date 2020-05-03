from django.contrib import admin
from .models import Student, StudentStatus, Teacher, TeacherStatus

admin.site.register(StudentStatus)
admin.site.register(Student)
admin.site.register(TeacherStatus)
admin.site.register(Teacher)