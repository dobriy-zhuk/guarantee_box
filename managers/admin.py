from django.contrib import admin

from managers.models import CurrencyExchange, Manager, MoneyTransaction
from students.models import Teacher

admin.site.register(CurrencyExchange)
admin.site.register(MoneyTransaction)


class TeacherInline(admin.StackedInline):
    model = Teacher


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    inlines = [TeacherInline]
