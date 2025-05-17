from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from .mixins import HTMXModalMixin
from .models import BillingType, PaymentInterval, ServiceType, Technology
from .forms import BillingTypeForm, PaymentIntervalForm, ServiceTypeForm, TechnologyForm
from apps.clients_suppliers.models import Party
from apps.clients_suppliers.forms import PartyForm

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
        html = render_to_string(
            'manager/partials/option_oob.html',
            {
            'new': new,
            'select_id': f'id_{self.lookup_field}'
            }
        )
        response = HttpResponse(html)
        response['HX-Trigger'] = 'closeModal'
        return response

class PaymentIntervalCreateModalView(HTMXModalMixin, CreateView):
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
        response = HttpResponse(html)
        response['HX-Trigger'] = 'closeModal'
        return response

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
        response = HttpResponse(html)
        response['HX-Trigger'] = 'closeModal'
        return response
    
class TechnologyCreateModalView(HTMXModalMixin, CreateView):
    model = Technology
    form_class = TechnologyForm
    template_name = 'manager/modals/add_option_form.html'
    modal_title = 'Add Technology'
    lookup_field = 'technologies'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = self.modal_title
        return ctx

    def form_valid(self, form):
        new = form.save()
        html = render_to_string('manager/partials/option_oob.html',
            {
            'new': new,
            'select_id': f'id_{self.model.lookup_field}'
            }
        )
        response = HttpResponse(html)
        response['HX-Trigger'] = 'closeModal'
        return response


class PartyCreateModalView(HTMXModalMixin, CreateView):
    model = Party
    form_class = PartyForm
    template_name = 'manager/modals/add_option_form.html'