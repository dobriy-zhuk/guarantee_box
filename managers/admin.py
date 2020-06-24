from django.contrib import admin

from managers.models import CurrencyExchange, Manager, MoneyTransaction
from students.models import Teacher

admin.site.register(CurrencyExchange)


@admin.register(MoneyTransaction)
class MoneyTransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'currency', 'action', 'comment']


class TeacherInline(admin.StackedInline):
    model = Teacher


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    inlines = [TeacherInline]
