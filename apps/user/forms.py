from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=255)
    password = forms.CharField(required=True, max_length=64, widget=forms.PasswordInput)
