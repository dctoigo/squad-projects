from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ('title','get_client','contract','start_date','due_date')
    list_filter   = ('contract__client','contract')
    search_fields = ('title','contract__code','client__name')
    filter_horizontal = ('technologies',)

    def get_client(self, obj):
        return obj.client or obj.contract.client
    get_client.short_description = 'Client'