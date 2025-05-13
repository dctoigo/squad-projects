from django.contrib import admin
from .models import Contract

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display    = ('code','client','billing_type','payment_interval','start_date','due_date')
    list_filter     = ('billing_type','payment_interval','client')
    search_fields   = ('code','client__name')
    filter_horizontal = ('technologies','service_types')