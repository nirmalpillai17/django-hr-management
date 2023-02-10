from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import *

WIDGET_CONFIG = {
    "first_name": forms.TextInput(attrs={"style": "text-transform: capitalize;"}),
    "last_name": forms.TextInput(attrs={"style": "text-transform: capitalize;"}),
    "mobile": forms.TextInput(attrs={"pattern": "^[6-9]\d{9}$"}),
    "emp_id": forms.TextInput(attrs={"pattern": "^[A-Za-z]{3}\d{5}$"}),
}


class AdminSignUp(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["email"].required = True

    class Meta(UserCreationForm):
        model = Admin
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "mobile",
            "org",
            "emp_id",
        )
        widgets = WIDGET_CONFIG


class ManagerSignUp(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["email"].required = True

    class Meta(UserCreationForm):
        model = Manager
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "mobile",
            "emp_id",
            "my_admin",
        )
        labels = {"my_admin": "Admin"}
        widgets = WIDGET_CONFIG


class HRSignUp(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["email"].required = True

    class Meta(UserCreationForm):
        model = HRManager
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "mobile",
            "emp_id",
            "my_admin",
        )
        labels = {"my_admin": "Admin"}
        widgets = WIDGET_CONFIG


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
