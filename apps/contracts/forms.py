from django import forms
from .models import Contract


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = [
            'client',
            'start_date', 'due_date',
            'billing_type', 'payment_interval',
            'technologies', 'service_types',
            'scope', 'milestones',
        ]
        widgets = {
            # datas com input nativo + Bootstrap
            'start_date':      forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'due_date':        forms.DateInput(attrs={'type':'date','class':'form-control'}),

            # selects com Bootstrap
            'client':          forms.Select(attrs={'class':'form-select'}),
            'billing_type':    forms.Select(attrs={'class':'form-select'}),
            'payment_interval':forms.Select(attrs={'class':'form-select'}),

            # múltipla escolha M2M
            'technologies':    forms.SelectMultiple(attrs={'class':'form-select','size':6}),
            'service_types':   forms.SelectMultiple(attrs={'class':'form-select','size':6}),

            # textos longos
            'scope':           forms.Textarea(attrs={'class':'form-control','rows':4}),
            'milestones':      forms.Textarea(attrs={'class':'form-control','rows':4}),
        }