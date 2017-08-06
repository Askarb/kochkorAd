from django import forms
from .models import Ad


class CreateAdForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    phone1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

