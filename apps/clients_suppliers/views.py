from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from .models import Party, Contact

# — Party Views —

class PartyListView(ListView):
    model = Party
    context_object_name = 'parties'
    template_name = 'clients_suppliers/party_list.html'
    queryset = Party.objects.filter(is_active=True).order_by('name')

class PartyDetailView(DetailView):
    model = Party
    context_object_name = 'party'
    template_name = 'clients_suppliers/party_detail.html'

class PartyCreateView(CreateView):
    model = Party
    fields = [
        'name','legal_name','type','is_active','cnpj',
        'address','state','city','phone_number','billing_email','notes'
    ]
    template_name = 'clients_suppliers/party_form.html'
    success_url = reverse_lazy('clients_suppliers:party_list')

class PartyUpdateView(UpdateView):
    model = Party
    fields = [
        'name','legal_name','type','is_active','cnpj',
        'address','state','city','phone_number','billing_email','notes'
    ]
    template_name = 'clients_suppliers/party_form.html'
    success_url = reverse_lazy('clients_suppliers:party_list')

class PartyDeleteView(DeleteView):
    model = Party
    template_name = 'clients_suppliers/party_confirm_delete.html'
    success_url = reverse_lazy('clients_suppliers:party_list')


# — Contact Views —

class ContactCreateView(CreateView):
    model = Contact
    fields = ['name','email','phone_number','position']
    template_name = 'clients_suppliers/contact_form.html'

    def form_valid(self, form):
        party = Party.objects.get(pk=self.kwargs['party_pk'])
        form.instance.party = party
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('clients_suppliers:party_detail', args=[self.kwargs['party_pk']])

class ContactUpdateView(UpdateView):
    model = Contact
    fields = ['name','email','phone_number','position']
    template_name = 'clients_suppliers/contact_form.html'

    def get_success_url(self):
        return reverse('clients_suppliers:party_detail', args=[self.object.party.pk])

class ContactDeleteView(DeleteView):
    model = Contact
    template_name = 'clients_suppliers/contact_confirm_delete.html'

    def get_success_url(self):
        return reverse('clients_suppliers:party_detail', args=[self.kwargs['party_pk']])