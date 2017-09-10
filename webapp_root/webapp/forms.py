from django import forms
from .models import Category


class CreateAdForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(
        Category.objects.all()
    )
    phone1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

