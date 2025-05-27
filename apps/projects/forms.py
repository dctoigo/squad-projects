from django import forms
from .models import Project
from ..contracts.models import Contract

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'status', 'contract', 'client', 'scope', 'main_contact',
            'billing_type', 'payment_interval', 'rate_or_value',
            'start_date', 'due_date', 'technologies'
        ]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'due_date':   forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'scope':      forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'main_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'rate_or_value': forms.NumberInput(attrs={'class': 'form-control'}),
            'technologies': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 6}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            contract = self.initial.get('contract') or self.instance.contract

            # Se for um ID (int), converte em instância
            if isinstance(contract, int):
                try:
                    contract = Contract.objects.get(pk=contract)
                except Contract.DoesNotExist:
                    contract = None

            if contract:
                self.fields['client'].disabled = True
                self.fields['billing_type'].disabled = True
                self.fields['payment_interval'].disabled = True
                self.fields['rate_or_value'].disabled = True

                self.initial['client'] = contract.client
                self.initial['billing_type'] = contract.billing_type
                self.initial['payment_interval'] = contract.payment_interval
                self.initial['rate_or_value'] = contract.value