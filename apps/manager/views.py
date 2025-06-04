from datetime import timedelta, datetime
from calendar import month_name
from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models import Sum, ExpressionWrapper, F, DurationField, Count, Q
from django.utils.timezone import localtime, now
from django.db.models.functions import TruncMonth

from .mixins import HTMXModalMixin
from .models import BillingType, PaymentInterval, ServiceType, Technology
from .forms import BillingTypeForm, PaymentIntervalForm, ServiceTypeForm, TechnologyForm
from apps.clients_suppliers.models import Party
from apps.clients_suppliers.forms import PartyForm
from apps.projects.models import Project
from apps.contracts.models import Contract
from apps.tasks.models import Task, TimeSession

import json


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # === ESTATÍSTICAS RÁPIDAS ===
        # CORRIGIDO: Party.type ao invés de party_type
        context['total_clients'] = Party.objects.filter(type='client').count()
        context['total_projects'] = Project.objects.filter(status='active').count()
        context['pending_tasks'] = Task.objects.filter(status__in=['todo', 'in_progress']).count()
        context['total_contracts'] = Contract.objects.filter(
            start_date__lte=now().date(),
            end_date__gte=now().date()
        ).count()

        # === ATIVIDADES RECENTES ===
        context['recent_activities'] = self.get_recent_activities()

        # === PRÓXIMOS PRAZOS ===
        context['upcoming_deadlines'] = self.get_upcoming_deadlines()

        # === MÉTRICAS ADICIONAIS ===
        context['total_tasks'] = Task.objects.count()
        context['completed_tasks'] = Task.objects.filter(status='done').count()
        context['active_sessions'] = TimeSession.objects.filter(stopped_at__isnull=True).count()
        
        # Calcular total de horas trabalhadas no mês atual
        current_month = now().month
        current_year = now().year
        monthly_sessions = TimeSession.objects.filter(
            started_at__month=current_month,
            started_at__year=current_year,
            stopped_at__isnull=False
        ).annotate(
            duration=ExpressionWrapper(F("stopped_at") - F("started_at"), output_field=DurationField())
        )
        
        total_duration = monthly_sessions.aggregate(total=Sum("duration"))["total"] or timedelta()
        context['monthly_hours'] = round(total_duration.total_seconds() / 3600, 1)

        # === PROJETOS POR STATUS ===
        context['projects_by_status'] = {
            'active': Project.objects.filter(status='active').count(),
            # CORRIGIDO: Removido 'planning' que não existe no model
            'inactive': Project.objects.filter(status='inactive').count(),
            'completed': Project.objects.filter(status='completed').count(),
            'cancelled': Project.objects.filter(status='cancelled').count(),
        }

        # === TAREFAS POR URGÊNCIA (não prioridade) ===
        # CORRIGIDO: urgency ao invés de priority
        context['tasks_by_urgency'] = {
            'high': Task.objects.filter(urgency='high').count(),
            'medium': Task.objects.filter(urgency='medium').count(),
            'low': Task.objects.filter(urgency='low').count(),
        }

        return context

    def get_recent_activities(self):
        """Retorna atividades recentes do sistema"""
        activities = []
        
        # Projetos criados recentemente (últimos 7 dias)
        # CORRIGIDO: title ao invés de name
        recent_projects = Project.objects.filter(
            created_at__gte=now() - timedelta(days=7)
        ).order_by('-created_at')[:3]
        
        for project in recent_projects:
            activities.append({
                'type': 'project_created',
                'icon': 'bi-plus-circle',
                'color': 'primary',
                'title': f'Novo projeto "{project.title}" criado',
                'time': project.created_at,
                'url': f'/projects/{project.code}/' if hasattr(project, 'get_absolute_url') else '#'
            })

        # Tarefas concluídas recentemente
        # CORRIGIDO: description ao invés de title
        completed_tasks = Task.objects.filter(
            status='done',
            updated_at__gte=now() - timedelta(days=7)
        ).select_related('project').order_by('-updated_at')[:3]
        
        for task in completed_tasks:
            activities.append({
                'type': 'task_completed',
                'icon': 'bi-check-circle',
                'color': 'success',
                'title': f'Tarefa "{task.description[:50]}..." concluída',
                'subtitle': f'Projeto: {task.project.title}',
                'time': task.updated_at,
                'url': f'/tasks/{task.id}/' if hasattr(task, 'get_absolute_url') else '#'
            })

        # Contratos próximos ao vencimento
        # CORRIGIDO: due_date ao invés de end_date
        expiring_contracts = Contract.objects.filter(
            due_date__gte=now().date(),
            due_date__lte=now().date() + timedelta(days=30)
        ).select_related('client').order_by('due_date')[:2]
        
        for contract in expiring_contracts:
            days_left = (contract.due_date - now().date()).days
            activities.append({
                'type': 'contract_expiring',
                'icon': 'bi-clock',
                'color': 'warning',
                'title': f'Contrato "{contract.code}" vence em {days_left} dias',
                'subtitle': f'Cliente: {contract.client.name}',
                'time': datetime.combine(contract.due_date, datetime.min.time()),
                'url': f'/contracts/{contract.code}/' if hasattr(contract, 'get_absolute_url') else '#'
            })

        # Ordenar por tempo (mais recente primeiro)
        activities.sort(key=lambda x: x['time'], reverse=True)
        
        return activities[:5]  # Retornar apenas os 5 mais recentes

    def get_upcoming_deadlines(self):
        """Retorna próximos prazos importantes"""
        deadlines = []
        
        # Tarefas com deadline próximo
        # CORRIGIDO: deadline é DateTimeField, comparar com date()
        upcoming_tasks = Task.objects.filter(
            deadline__date__gte=now().date(),
            deadline__date__lte=now().date() + timedelta(days=14),
            status__in=['todo', 'in_progress']
        ).select_related('project').order_by('deadline')[:5]
        
        for task in upcoming_tasks:
            # CORRIGIDO: deadline.date() para comparação
            days_left = (task.deadline.date() - now().date()).days
            
            if days_left <= 1:
                urgency = 'danger'
                urgency_text = 'Urgente' if days_left == 0 else 'Amanhã'
            elif days_left <= 3:
                urgency = 'warning'
                urgency_text = f'{days_left} dias'
            else:
                urgency = 'info'
                urgency_text = f'{days_left} dias'
            
            # Calcular progresso baseado no status
            if task.status == 'done':
                progress = 100
            elif task.status == 'in_progress':
                progress = 50
            else:
                progress = 10
                
            deadlines.append({
                'title': task.description[:30] + '...' if len(task.description) > 30 else task.description,
                'project': task.project.title,
                'deadline': task.deadline.date(),
                'urgency': urgency,
                'urgency_text': urgency_text,
                'progress': progress,
                'url': f'/tasks/{task.id}/' if hasattr(task, 'get_absolute_url') else '#'
            })

        # Projetos com deadline próximo
        # CORRIGIDO: due_date ao invés de end_date
        upcoming_projects = Project.objects.filter(
            due_date__gte=now().date(),
            due_date__lte=now().date() + timedelta(days=14),
            status='active'
        ).order_by('due_date')[:3]
        
        for project in upcoming_projects:
            days_left = (project.due_date - now().date()).days
            
            if days_left <= 1:
                urgency = 'danger'
                urgency_text = 'Urgente'
            elif days_left <= 7:
                urgency = 'warning'
                urgency_text = f'{days_left} dias'
            else:
                urgency = 'info'
                urgency_text = f'{days_left} dias'
            
            # Calcular progresso baseado nas tarefas concluídas
            total_tasks = project.tasks.count()
            completed_tasks = project.tasks.filter(status='done').count()
            progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
                
            deadlines.append({
                'title': f'Projeto: {project.title}',
                'project': project.client.name if project.client else 'Cliente não definido',
                'deadline': project.due_date,
                'urgency': urgency,
                'urgency_text': urgency_text,
                'progress': round(progress),
                'url': f'/projects/{project.code}/' if hasattr(project, 'get_absolute_url') else '#'
            })

        return sorted(deadlines, key=lambda x: x['deadline'])[:6]


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