from django.contrib import admin

from managers.models import CurrencyExchange, Manager

admin.site.register(Manager)
admin.site.register(CurrencyExchange)
