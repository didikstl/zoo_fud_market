from django import forms

from apps.user.models import User


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=255)
    password = forms.CharField(required=True, max_length=64, widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password_confirm = forms.CharField(required=True, max_length=64, widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        check = User.objects.filter(email=email)
        if check:
            raise forms.ValidationError('Пользователь с таким E-mail уже существует')


    class Meta:
        model = User
        fields = ['username', 'image', 'first_name', 'last_name', 'email', 'phone', 'password', 'password_confirm']
