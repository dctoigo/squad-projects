from django.contrib import admin
from .models import Technology, ServiceType, BillingType, PaymentInterval

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(BillingType)
class BillingTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(PaymentInterval)
class PaymentIntervalAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
