from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class SignUPForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "input",
                "placeholder": "Type here",
                }),
            "password": forms.PasswordInput(attrs={
                    "class": "input",
                    "placeholder": "Type here",
                }),
        }

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(label="Username", widget=forms.TextInput(attrs={"autofocus": True, "class": "input"}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "input"}),
    )
    