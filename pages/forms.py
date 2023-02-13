from django import forms

from .models import *


# date input field
class DateInput(forms.DateInput):
    input_type = "date"


class EmployeeDetails(forms.ModelForm):
    class Meta:
        model = NewEmployees
        fields = [
            "first_name",
            "last_name",
            "email",
            "mobile",
            "gender",
            "dob",
            "my_manager",
            "start_date",
            "quit_date",
        ]
        labels = {"my_manager": "Manager"}
        widgets = {
            "first_name": forms.TextInput(
                attrs={"style": "text-transform: capitalize;"}
            ),
            "last_name": forms.TextInput(
                attrs={"style": "text-transform: capitalize;"}
            ),
            "mobile": forms.TextInput(attrs={"pattern": "^[6-9]\d{9}$"}),
            "dob": DateInput(),
            "start_date": DateInput(),
            "quit_date": DateInput(),
        }
