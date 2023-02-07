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
            "start_date",
            "quit_date",
        ]

        widgets = {
            "dob": DateInput(),
            "start_date": DateInput(),
            "quit_date": DateInput(),
        }
