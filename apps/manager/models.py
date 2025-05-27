from django.db import models

class Technology(models.Model):
    name = models.CharField('Name', max_length=64, unique=True)
    def __str__(self): return self.name

class ServiceType(models.Model):
    name = models.CharField('Name', max_length=64, unique=True)
    def __str__(self): return self.name

class BillingType(models.Model):
    CHOICE_MODE = (
        ('fixed', 'Valor Fixo'),
        ('hourly', 'Valor por Hora'),
    )
    name = models.CharField('Name', max_length=64, unique=True)
    mode = models.CharField('Mode', max_length=64, choices=CHOICE_MODE, default='fixed')
    def __str__(self): return self.name

class PaymentInterval(models.Model):
    name = models.CharField('Name', max_length=64, unique=True)
    def __str__(self): return self.name