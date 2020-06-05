from django.contrib import admin
from courses.models import Subject, Course, Module, LessonRoom


@admin.register(LessonRoom)
class LessonRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'lesson_name', 'display_students']
    filter_horizontal = ['students']

    def display_students(self, obj):
        return ', '.join([
            student.name for student in obj.students.all()
        ])
    display_students.short_description = 'Students'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
