from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Contract
from .forms import ContractForm
class ContractListView(ListView):
    model = Contract
    template_name = 'contracts/contract_list.html'
    context_object_name = 'contracts'
    paginate_by = 10

    def get_queryset(self):
        qs = Contract.objects.select_related('client', 'billing_type', 'payment_interval')
        return qs.order_by('-start_date')

class ContractDetailView(DetailView):
    model = Contract
    template_name = 'contracts/contract_detail.html'
    context_object_name = 'contract'

class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    # fields = [
    #     'client','start_date','due_date',
    #     'billing_type','payment_interval',
    #     'technologies','service_types',
    #     'scope','milestones'
    # ]
    template_name = 'contracts/contract_form.html'
    success_url = reverse_lazy('contracts:contract_list')

class ContractUpdateView(UpdateView):
    model = Contract
    form_class = ContractForm
    # fields = [
    #     'client','start_date','due_date',
    #     'billing_type','payment_interval',
    #     'technologies','service_types',
    #     'scope','milestones'
    # ]
    template_name = 'contracts/contract_form.html'
    success_url = reverse_lazy('contracts:contract_list')

class ContractDeleteView(DeleteView):
    model = Contract
    template_name = 'contracts/contract_confirm_delete.html'
    success_url = reverse_lazy('contracts:contract_list')