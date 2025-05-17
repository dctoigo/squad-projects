# apps/clients_suppliers/forms.py

from django import forms
from .models import Party, Contact

class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = [
            'name', 'legal_name', 'type', 'is_active', 'cnpj',
            'address', 'state', 'city', 'phone_number', 'billing_email', 'notes'
        ]
        widgets = {
            'name':          forms.TextInput(attrs={'class': 'form-control'}),
            'legal_name':    forms.TextInput(attrs={'class': 'form-control'}),
            'type':          forms.Select(attrs={'class': 'form-select'}),
            'is_active':     forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cnpj':          forms.TextInput(attrs={'class': 'form-control'}),
            'address':       forms.TextInput(attrs={'class': 'form-control'}),
            'state':         forms.TextInput(attrs={'class': 'form-control'}),
            'city':          forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number':  forms.TextInput(attrs={'class': 'form-control'}),
            'billing_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'notes':         forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['party', 'name', 'position', 'email', 'phone_number']
        widgets = {
            'party':        forms.Select(attrs={'class': 'form-select'}),
            'name':         forms.TextInput(attrs={'class': 'form-control'}),
            'position':     forms.TextInput(attrs={'class': 'form-control'}),
            'email':        forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }