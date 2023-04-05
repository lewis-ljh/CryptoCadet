from django import forms
from .models import Ticket

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField(required=False)

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'query']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'query': forms.Textarea(attrs={'class': 'form-control'}), 
        }

