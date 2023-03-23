from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Login')
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', strip=False, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirm password', strip=False, required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'first_name', 'last_name', 'email')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match!')

        if not first_name and not last_name:
            raise forms.ValidationError('At least one of the fields (first_name, last_name) must be filled.')

        if not email:
            raise forms.ValidationError('Email is required.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

