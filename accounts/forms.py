from django.contrib.auth.forms import UserCreationForm

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
