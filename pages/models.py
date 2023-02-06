from django.db import models
from django.core.validators import RegexValidator


class NewEmployees(models.Model):
    first_name = models.CharField("First Name", max_length=50, null=False, blank=False)
    last_name = models.CharField("Last Name", max_length=50, null=True, blank=True)

    email = models.EmailField("Email", null=False, blank=False)
    mobile = models.CharField(
        "Mobile No.",
        validators=[
            RegexValidator(
                regex="^[6-9]\d{9}$",
                message="Invalid Indian mobile number!",
                code="invalid",
            )
        ],
        max_length=10,
        null=False,
        blank=False,
    )

    gender_type = (
        ("M", "Male"),
        ("F", "Female"),
    )

    gender = models.CharField(
        max_length=1, choices=gender_type, null=False, blank=False
    )
    dob = models.DateField("Date Of Birth", null=False, blank=False)
    start_date = models.DateField("Start Date", null=False, blank=False)
    quit_date = models.DateField("Quit Date", null=True, blank=True)
