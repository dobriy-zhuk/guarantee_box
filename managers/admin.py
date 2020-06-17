from django.contrib import admin

from managers.models import CurrencyExchange, Manager, MoneyTransaction

admin.site.register(Manager)
admin.site.register(CurrencyExchange)
admin.site.register(MoneyTransaction)
