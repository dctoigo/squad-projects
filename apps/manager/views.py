from datetime import timedelta
from calendar import month_name
from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models import Sum, ExpressionWrapper, F, DurationField
from django.utils.timezone import localtime

from .mixins import HTMXModalMixin
from .models import BillingType, PaymentInterval, ServiceType, Technology
from .forms import BillingTypeForm, PaymentIntervalForm, ServiceTypeForm, TechnologyForm
from apps.clients_suppliers.models import Party
from apps.clients_suppliers.forms import PartyForm
from apps.projects.models import Project
from apps.tasks.models import Task, TimeSession

from collections import defaultdict

import json


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/dashboard.html'


class DashboardTasksView(TemplateView):
    template_name = 'manager/dashboard_tasks_new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filtros via query params
        client_id = self.request.GET.get('client')
        task_status = self.request.GET.get('task_status')
        start_date = self.request.GET.get('start')
        end_date = self.request.GET.get('end')

        grouped = defaultdict(list)

        # Base queryset com otimização
        projects_qs = Project.objects.select_related('client').prefetch_related(
            'tasks',
            'tasks__responsible',
            'tasks__time_sessions'
        )

        if client_id:
            projects_qs = projects_qs.filter(client_id=client_id)

        for project in projects_qs:
            # Usar os métodos helpers do modelo Project
            tasks = project.exclude_closed if task_status != 'closed' else project.closed
            
            if task_status and task_status != 'closed':
                tasks = tasks.filter(status=task_status)

            # Filtrar sessions se necessário
            if start_date or end_date:
                tasks = tasks.filter(
                    time_sessions__started_at__date__range=[start_date or '1900-01-01', 
                                                          end_date or '9999-12-31']
                ).distinct()

            project.filtered_tasks = tasks
            grouped[project.client].append(project)

        context['grouped'] = dict(grouped)

        # Dados para os filtros no template
        context['clients'] = Party.objects.all()
        context['task_status_choices'] = Task._meta.get_field('status').choices

        # Repopular os campos do filtro no template
        context.update({
            'filter_client': client_id,
            'filter_status': task_status,
            'filter_start': start_date,
            'filter_end': end_date,
        })

        return context

# — Profile View —
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name','last_name','email']
    template_name = 'manager/profile.html'
    success_url = reverse_lazy('manager:profile')

    def get_object(self):
        return self.request.user


# — Lookup Modal Views —
class BillingTypeCreateModalView(HTMXModalMixin, CreateView):
    model = BillingType
    form_class = BillingTypeForm
    template_name = 'manager/modals/add_option_form.html'
    modal_title = 'Add Billing Type'
    lookup_field = 'billing_type'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.modal_title
        return ctx


    def form_valid(self, form):
        new = form.save()
        html = render_to_string('manager/partials/option_oob.html',
            {
            'new': new,
            'select_id': f'id_{self.lookup_field}'
            }
        )
        # response = HttpResponse(html)
        response = HttpResponse(html, status=204)
        response['HX-Trigger'] = json.dumps({
            "closeModal": None,
            "refreshBillingType": None
        })

        # response['HX-Trigger'] = 'closeModal'
        return response
    
    def get_lookup_field(self):
        return self.lookup_field

    def get_oob_template(self):
        return 'manager/partials/option_oob.html'


def billingtype_select_options(request):
    options = BillingType.objects.all()
    html = render_to_string("manager/partials/select_options.html", {"options": options})
    return HttpResponse(html)


class PaymentIntervalCreateModalView( CreateView):
    model = PaymentInterval
    form_class = PaymentIntervalForm
    template_name = 'manager/modals/add_option_form.html'
    modal_title = 'Add Payment Interval'
    lookup_field = 'payment_interval'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.modal_title
        return ctx

    def form_valid(self, form):
        new = form.save()
        html = render_to_string('manager/partials/option_oob.html',
            {
            'new': new,
            'select_id': f'id_{self.lookup_field}'
            }
        )
        # response = HttpResponse(html)
        response = HttpResponse(html, status=204)
        response['HX-Trigger'] = json.dumps({
            "closeModal": None,
            "refreshPaymentInterval": None
        })

        # response['HX-Trigger'] = 'closeModal'
        return response
    
    def get_lookup_field(self):
        return self.lookup_field

    def get_oob_template(self):
        return 'manager/partials/option_oob.html'


def paymentinterval_select_options(request):
    options = PaymentInterval.objects.all()
    html = render_to_string("manager/partials/select_options.html", {"options": options})
    return HttpResponse(html)


class ServiceTypeCreateModalView(HTMXModalMixin, CreateView):
    model = ServiceType
    form_class = ServiceTypeForm
    template_name = 'manager/modals/add_option_form.html'
    modal_title = 'Add Service Type'
    lookup_field = 'service_types'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.modal_title
        return ctx

    def form_valid(self, form):
        new = form.save()
        html = render_to_string('manager/partials/option_oob.html',
            {
            'new': new,
            'select_id': f'id_{self.lookup_field}'
            }
        )
        # response = HttpResponse(html)
        response = HttpResponse(html, status=204)
        response['HX-Trigger'] = json.dumps({
            "closeModal": None,
            "refreshServiceType": None
        })

        # response['HX-Trigger'] = 'closeModal'
        return response
    
    def get_lookup_field(self):
        return self.lookup_field

    def get_oob_template(self):
        return 'manager/partials/option_oob.html'


def servicetype_select_options(request):
    options = ServiceType.objects.all()
    html = render_to_string("manager/partials/select_options.html", {"options": options})
    return HttpResponse(html)


class TechnologyCreateModalView(HTMXModalMixin, CreateView):
    model = Technology
    form_class = TechnologyForm
    template_name = 'manager/modals/add_option_form.html'
    modal_title = 'Add Technology'
    lookup_field = 'technology'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.modal_title
        return ctx

    def form_valid(self, form):
        new = form.save()
        html = render_to_string('manager/partials/option_oob.html',
            {
            'new': new,
            'select_id': f'id_{self.lookup_field}'
            }
        )
        # response = HttpResponse(html)
        response = HttpResponse(html, status=204)
        response['HX-Trigger'] = json.dumps({
            "closeModal": None,
            "refreshTechnology": None
        })

        # response['HX-Trigger'] = 'closeModal'
        return response
    
    def get_lookup_field(self):
        return self.lookup_field

    def get_oob_template(self):
        return 'manager/partials/option_oob.html'


def technology_select_options(request):
    options = Technology.objects.all()
    html = render_to_string("manager/partials/select_options.html", {"options": options})
    return HttpResponse(html)


class PartyCreateModalView(HTMXModalMixin, CreateView):
    model = Party
    form_class = PartyForm
    template_name = 'manager/modals/add_option_form.html'
    modal_title = 'Add Party'
    lookup_field = 'client'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.modal_title
        return ctx

    def form_valid(self, form):
        new = form.save()
        html = render_to_string('manager/partials/option_oob.html',
            {
            'new': new,
            'select_id': f'id_{self.lookup_field}'
            }
        )
        # response = HttpResponse(html)
        response = HttpResponse(html, status=204)
        response['HX-Trigger'] = json.dumps({
            "closeModal": None,
            "refreshParty": None
        })

        # response['HX-Trigger'] = 'closeModal'
        return response
    
    def get_lookup_field(self):
        return self.lookup_field

    def get_oob_template(self):
        return 'manager/partials/option_oob.html'
    
def party_select_options(request):
    options = Party.objects.all()
    html = render_to_string("manager/partials/select_options.html", {"options": options})
    return HttpResponse(html)

class DashboardExecutiveView(TemplateView):
    template_name = 'manager/dashboard_executive.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        month = self.request.GET.get("month")
        year = self.request.GET.get("year")

        # Anotar duração real
        sessions = TimeSession.objects.exclude(stopped_at__isnull=True).annotate(
            duration=ExpressionWrapper(F("stopped_at") - F("started_at"), output_field=DurationField())
        )

        if month:
            sessions = sessions.filter(started_at__month=month)
        if year:
            sessions = sessions.filter(started_at__year=year)

        # Total de horas
        total_duration = sessions.aggregate(total=Sum("duration"))["total"] or timedelta()
        context["total_hours"] = round(total_duration.total_seconds() / 3600, 1)

        # Outras métricas
        context["active_projects"] = Project.objects.filter(status="active").count()
        context["open_tasks"] = Task.objects.filter(status="todo").count()
        context["completed_tasks"] = Task.objects.filter(status="done").count()
        context["active_sessions"] = TimeSession.objects.filter(stopped_at__isnull=True).count()

        # Dados para gráfico
        grouped = defaultdict(float)
        for s in sessions:
            dt = localtime(s.started_at)
            label = f"{month_name[dt.month]} {dt.year}"
            grouped[label] += s.duration.total_seconds() / 3600 if s.duration else 0

        ordered = sorted(grouped.items(), key=lambda x: x[0])
        context["chart_labels"] = [label for label, _ in ordered]
        context["chart_data"] = [round(hours, 1) for _, hours in ordered]

        # Dados para os filtros
        all_years = TimeSession.objects.dates('started_at', 'year')
        context["years"] = [y.year for y in all_years]
        context["filter_month"] = month
        context["filter_year"] = year

        return context
    

class ClientDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'manager/dashboard_client_view.html'

    def test_func(self):
        # Usuário está vinculado a um cliente
        return hasattr(self.request.user, 'party')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        client = getattr(user, 'party', None)

        grouped = defaultdict(list)

        if client:
            projects = Project.objects.filter(client=client).prefetch_related('tasks__time_sessions')
            for project in projects:
                project.filtered_tasks = project.tasks.all()
                project.sessions = TimeSession.objects.filter(task__project=project)
                grouped[client].append(project)

        context['grouped'] = dict(grouped)
        return context