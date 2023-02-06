from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import *


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


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

