from django import forms
from .models import Ad


class CreateAdForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(
        attrs={'value': 'asd', 'multiple': True, 'class': 'form-control',
                                   }),
        required=False)

    class Meta:
        model = Ad
        fields = ('title', 'text', 'category', 'phone1', 'phone2')

