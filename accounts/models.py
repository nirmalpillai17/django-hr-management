from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    mobile = models.CharField(
        "Mobile No.",
        validators=[
            RegexValidator(
                regex="^[6-9]\d{9}$",
                message="Invalid Indian mobile number!",
            )
        ],
        max_length=10,
        null=False,
        blank=False,
    )

    emp_id = models.CharField(
        "Employee ID",
        validators=[
            RegexValidator(
                regex="^[A-Za-z]{3}\d{5}$",
                message="Invalid Employee ID! Should be of form ABC12345.",
            )
        ],
        max_length=8,
        null=False,
        blank=False,
    )


class Admin(User):
    # username
    # first_name
    # last_name
    # email
    # mobile
    # org
    # emp_id
    org = models.CharField("Organization", max_length=50, null=False, blank=False)

class Manager(User):
    # username
    # first_name
    # last_name
    # email
    # mobile
    
    my_admin = models.ForeignKey(Admin, on_delete=models.CASCADE)

class HR(User):
    pass

class Employee(User):
    pass
