
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from apps.manager.views import DashboardView, DashboardTasksView


urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
    path('dashboard/tasks/', DashboardTasksView.as_view(), name='dashboard_tasks'),
    path('admin/', admin.site.urls),
    path('about/', TemplateView.as_view(template_name='manager/about.html'), name='about_chronos'),
    
    # Apps do Projeto
    path('accounts/', include('apps.manager.urls', namespace='manager')),
    path('party/', include('apps.clients_suppliers.urls')),
    path('contracts/', include('apps.contracts.urls')),
    path('projects/', include('apps.projects.urls')),
    # path('finance/', include('apps.finance.urls')),
    # path('accounting/', include('apps.accounting.urls')),
    # path('integrations/', include('apps.integrations.urls')),
    path('tasks/', include('apps.tasks.urls')),
]

# Login / Logout / Profile


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)