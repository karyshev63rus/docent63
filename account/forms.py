from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'email': 'Адрес эл. почты',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Пароли не совпадают")
        return cd['password2']


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control'}
            ),
        }


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'address', 'postal_code', 'city', 'country')
        widgets = {
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'address': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'postal_code': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'city': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'country': forms.TextInput(
                attrs={'class': 'form-control'}
            )
        }

