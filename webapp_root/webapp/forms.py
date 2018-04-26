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

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Там сатам'}),
            'text': forms.Textarea(attrs={'placeholder': '5 болмолуу там сатам...'}),
            'phone1': forms.TextInput(attrs={'placeholder': '0700 123 456'}),
            'phone2': forms.TextInput(attrs={'placeholder': '0700 123 457'}),
        }


