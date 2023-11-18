from .models import Profils, Image
from django.forms import ModelForm, TextInput, ImageField, DateTimeField


class ProfilsForm(ModelForm):
    class Meta:
        model = Profils
        fields = ['login', 'password']

        widgets = {
            'login': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль'
            }),
            'password': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль'
            }),
        }


class EnterProfilForm(ModelForm):
    class Meta:
        model = Profils
        fields = ['login', 'password']

        widgets = {
            'login': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль'
            }),
            'password': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль'
            }),
        }


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ['name']

        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название рисунка'
            }),
        }

