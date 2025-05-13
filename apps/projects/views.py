from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Project

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
    fields = [
        'title','contract','client','start_date','due_date',
        'billing_type','payment_interval','rate_or_value',
        'technologies','scope','main_contact'
    ]
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:project_list')

    def get_initial(self):
        initial = super().get_initial()
        contract_pk = self.request.GET.get('contract')
        if contract_pk:
            initial['contract'] = contract_pk
        return initial

class ProjectUpdateView(UpdateView):
    model = Project
    fields = [
        'title','contract','client','start_date','due_date',
        'billing_type','payment_interval','rate_or_value',
        'technologies','scope','main_contact'
    ]
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('projects:project_list')

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/project_confirm_delete.html'
    success_url = reverse_lazy('projects:project_list')