from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Ad, Message, AdImage, AdPhone


class CreateAdForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(
        attrs={'value': 'asd', 'multiple': True, 'class': 'form-control'}),
        required=False)

    class Meta:
        model = Ad
        fields = ('title', 'text', 'category')

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Там сатам')}),
            'text': forms.Textarea(attrs={'placeholder': _('5 болмолуу там сатам...')}),
        }


class AdImageUploadForm(forms.ModelForm):

    class Meta:
        model = AdImage
        fields = ['image', ]


class AdPhoneForm(forms.ModelForm):

    class Meta:
        model = AdPhone
        fields = ['phone', ]
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': _('Ваш номер телефона')})
        }


AdImageFormset = forms.inlineformset_factory(Ad, AdImage, extra=3, max_num=20, form=AdImageUploadForm)
AdPhoneFormset = forms.inlineformset_factory(Ad, AdPhone, extra=2, max_num=10, form=AdPhoneForm)


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
