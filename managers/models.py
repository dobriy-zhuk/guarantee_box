from django.db import models
from django.contrib.auth.models import User


class Roles(models.Model):
    name = models.CharField(max_length=200, default='Administrator')

    def __str__(self):
        return self.name


class Manager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.TextField(max_length=500, blank=True, default='712312')
    city = models.CharField(max_length=60, default='')
    role = models.ForeignKey(Roles, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CurrencyExchange(models.Model):
    """Describe managers_currensyexchange table in db.

    euro: how much rubles costs 1 euro
    dollar: how much rubles costs 1 dollar

    Max number is 999.99 for each field.

    """
    euro = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    dollar = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)

    def __str__(self):
        return 'Обмен валюты'
