
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Apps do Projeto
    path('party/', include('apps.clients_suppliers.urls')),
    # path('contracts/', include('apps.contracts.urls')),
    # path('finance/', include('apps.finance.urls')),
    # path('accounting/', include('apps.accounting.urls')),
    # path('integrations/', include('apps.integrations.urls')),
    # path('tasks/', include('apps.tasks.urls')),
    # path('projects/', include('apps.projects.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)