from django import forms
from .models import Ad, Message


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


class MessageCreateForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('name', 'email', 'phone', 'message')

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Сооронбай'}),
            'email': forms.TextInput(attrs={'placeholder': 'example@mail.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '0500123456'}),
            'message': forms.Textarea(attrs={'placeholder': 'Ваше сообщение...'}),
        }