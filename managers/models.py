from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.TextField(max_length=500, blank=True, default='712312')
    city = models.CharField(max_length=60, default='')
    email = models.EmailField(default='')

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


class MoneyTransaction(models.Model):
    """
    currency: RUB, USD or EUR

    amount: account balance, how much money does the student have
    Max number is 99999.99

    action (str): action what you want to do, it can be 'withdraw' or 'deposit'
    'withdraw' means 'снять (деньги)' and 'deposti' means 'внести (деньги)'.

    comment (str): you should to describe why you deposit or withdraw
    money from/to your account

    """

    class MoneyTransactionCurrency(models.TextChoices):
        RUBLE = 'RUB', _('Ruble')
        DOLLAR = 'USD', _('Dollar')
        EURO = 'EUR', _('Euro')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(default=0.00, max_digits=7, decimal_places=2)
    currency = models.CharField(
        max_length=3,
        choices=MoneyTransactionCurrency.choices,
        default=MoneyTransactionCurrency.RUBLE,
    )
    action = models.CharField(max_length=8)
    comment = models.CharField(max_length=200, default='')
