from django import forms

from .models import *


# date input field
class DateInput(forms.DateInput):
    input_type = "date"


class EditEmployeeDetails(forms.ModelForm):
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
            "dob": DateInput(),
            "start_date": DateInput(),
            "quit_date": DateInput(),
        }
