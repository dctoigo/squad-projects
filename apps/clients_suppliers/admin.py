from django.contrib import admin
from .models import Party, Contact

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_type_display', 'is_active', 'cnpj')
    list_filter = ['type', 'is_active']
    search_fields = ['name', 'legal_name', 'cnpj', 'city']
    ordering = ['name']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'party', 'email', 'phone_number', 'position')
    list_filter = ['party']
    search_fields = ['name', 'email', 'phone_number']
    ordering = ['name']