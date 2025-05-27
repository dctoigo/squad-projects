from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'description', 'urgency', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'urgency': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }