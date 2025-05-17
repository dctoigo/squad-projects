from django import forms
from .models import BillingType, PaymentInterval, ServiceType, Technology
# Note: PartyForm stays in clients_suppliers/forms.py

class BillingTypeForm(forms.ModelForm):
    class Meta:
        model = BillingType
        fields = ['name']

class PaymentIntervalForm(forms.ModelForm):
    class Meta:
        model = PaymentInterval
        fields = ['name']

class ServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = ['name']

class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = ['name']