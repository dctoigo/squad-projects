from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project
from .forms import ProjectForm
from ..contracts.models import Contract
from ..clients_suppliers.models import Party
from collections import defaultdict

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10

    def get_queryset(self):
        return Project.objects.select_related('contract','client').order_by('-start_date')

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'

    def get_initial(self):
        initial = super().get_initial()
        contract_id = self.request.GET.get('contract')
        if contract_id:
            try:
                contract = Contract.objects.get(pk=contract_id)
                initial.update({
                    'contract': contract,
                    'client': contract.client,
                    'billing_type': contract.billing_type,
                    'payment_interval': contract.payment_interval,
                    'rate_or_value': contract.value
                })
            except Contract.DoesNotExist:
                pass
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.GET.get('contract') or form.instance.contract:
            form.fields['client'].disabled = True
            form.fields['billing_type'].disabled = True
            form.fields['payment_interval'].disabled = True
            form.fields['rate_or_value'].disabled = True
        return form

    def get_success_url(self):
        return reverse_lazy('projects:project_list')

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Se houver contrato vinculado, desabilita os campos herdados
        if self.object.contract:
            form.fields['client'].disabled = True
            form.fields['billing_type'].disabled = True
            form.fields['payment_interval'].disabled = True
            form.fields['rate_or_value'].disabled = True
        return form

    def form_valid(self, form):
        # Garante herança dos dados do contrato ao salvar
        if form.instance.contract:
            form.instance.client = form.instance.contract.client
            form.instance.billing_type = form.instance.contract.billing_type
            form.instance.payment_interval = form.instance.contract.payment_interval
            form.instance.rate_or_value = form.instance.contract.value
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('projects:project_detail', kwargs={'pk': self.object.pk})

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 20

    def get_queryset(self):
        qs = Project.objects.select_related('client', 'contract')
        client = self.request.GET.get('client')
        status = self.request.GET.get('status')
        search = self.request.GET.get('search')

        if client:
            qs = qs.filter(client_id=client)

        if status:
            qs = qs.filter(status=status)

        if search:
            qs = qs.filter(title__icontains=search)

        return qs.order_by('-start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_mode = self.request.GET.get('view', 'simple')
        context['view_mode'] = view_mode

        if view_mode == 'grouped':
            grouped = defaultdict(lambda: defaultdict(list))
            for project in context['projects']:
                client_name = project.client.name if project.client else '—'
                contract = project.contract
                grouped[client_name][contract].append(project)

            context['grouped_projects'] = dict(grouped)

        # Para os filtros no template
        context['clients'] = Party.objects.all()
        context['status_choices'] = Project.STATUS_CHOICES
        return context
    
class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('projects:project_list')