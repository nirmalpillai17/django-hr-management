from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib import messages
import string
import random

from accounts.models import *
from .forms import *

ADD_EMP_DONE = "Add employee request sent successfully."
USER_CREATION_DONE = "User for employee created successfully."
# USER_CREATION_FAIL = "Sorry! An unexpected error occured. Please try again."


def if_admin(request):
    username = request.user.username
    if Admin.objects.all().filter(username=username).exists():
        return True
    return False


def if_manager(request):
    username = request.user.username
    if Manager.objects.all().filter(username=username).exists():
        return True
    return False


def if_hr(request):
    username = request.user.username
    if HRManager.objects.all().filter(username=username).exists():
        return True
    return False


def if_employee(request):
    username = request.user.username
    if Employee.objects.all().filter(username=username).exists():
        return True
    return False


def admin_home(request):
    if not (request.user.is_authenticated and if_admin(request)):
        return HttpResponse("Unauthorised access!")

    context = dict()
    context["title"] = "Home | Admin"
    context["heading"] = "Admin Home Page"
    username = request.user.username
    user = Admin.objects.all().get(username=username)
    context["user"] = user
    return render(request, "pages/admin_home.html", context)


def manager_home(request):
    if not (request.user.is_authenticated and if_manager(request)):
        return HttpResponse("Unauthorised access!")

    context = dict()
    context["title"] = "Home | Manager"
    context["heading"] = "Manager Home Page"
    username = request.user.username
    user = Manager.objects.all().get(username=username)
    context["user"] = user
    return render(request, "pages/manager_home.html", context)


def hr_home(request):
    if not (request.user.is_authenticated and if_hr(request)):
        return HttpResponse("Unauthorised access!")

    context = dict()
    context["title"] = "Home | HR"
    context["heading"] = "HR Home Page"
    username = request.user.username
    user = HRManager.objects.all().get(username=username)
    context["user"] = user
    return render(request, "pages/hr_home.html", context)


def employee_home(request):
    if not (request.user.is_authenticated and if_employee(request)):
        return HttpResponse("Unauthorised access!")

    context = dict()
    context["title"] = "Home | Employee"
    context["heading"] = "Employee Home Page"
    username = request.user.username
    user = Employee.objects.all().get(username=username)
    context["user"] = user
    return render(request, "pages/employee_home.html", context)


def user_creation(request):  # function for admins
    if not (request.user.is_authenticated and if_admin(request)):
        return HttpResponse("Unauthorised access!")

    context = dict()
    context["title"] = "Create User | Admin"
    context["heading"] = "Create User Requests"
    context["requests"] = NewEmployees.objects.all()
    return render(request, "admin/create_user.html", context)


def handle_request(request, pk):
    if not (request.user.is_authenticated and if_admin(request)):
        return HttpResponse("Unauthorised access!")

    user = NewEmployees.objects.all().get(id=pk)
    temp_name = user.first_name.lower()
    usernames = User.objects.values_list("username", flat=True)
    while True:
        random_num = str(random.randint(100, 999))
        if temp_name in usernames:
            username = "".join((temp_name, random_num))
        else:
            username = temp_name
            break

    ids = User.objects.values_list("emp_id", flat=True)
    while True:
        emp_id = "".join((user.my_manager.emp_id[:3], random_num, random_num[:2]))
        if emp_id in ids:
            random_num = str(random.randint(100, 999))
        else:
            break

    chars = "".join((string.ascii_letters, "!@#$%^&*()", "1234567890"))
    password = "".join((random.choice(chars) for _ in range(10)))

    # try:
    #   validate user creation
    Employee.objects.create_user(
        username=username,
        password=password,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        mobile=user.mobile,
        emp_id=emp_id,
        gender=user.gender,
        dob=user.dob,
        start_date=user.start_date,
        quit_date=user.quit_date,
        my_manager=user.my_manager,
    )
    user.delete()
    messages.success(request, USER_CREATION_DONE)

    # except:
    #   messages.error(request, USER_CREATION_FAIL)

    return redirect("create_user")


def dismiss_request(request, pk):
    if not (request.user.is_authenticated and if_admin(request)):
        return HttpResponse("Unauthorised access!")

    user = NewEmployees.objects.all().get(id=pk)
    user.delete()
    return redirect("create_user")


def add_employee(request):  # function for hr
    if not(request.user.is_authenticated and if_hr(request)):
        return HttpResponse("Unauthorised access!")

    context = dict()
    context["title"] = "New Employee | HR"
    context["heading"] = "Add Employee Page"
    form = EditEmployeeDetails(request.POST or None)
    context["form"] = form
    if request.method == "POST":
        if form.is_valid():
            fs = form.save(commit=False)
            fs.first_name = form.cleaned_data["first_name"].title()
            if fs.last_name:
                fs.last_name = form.cleaned_data["last_name"].title()
            fs.save()
            messages.success(request, ADD_EMP_DONE)
            return redirect("hr_home")
        for error_list in form.errors.values():
            for error in error_list:
                messages.warning(request, error)
            return redirect("add_employee")
    return render(request, "hr/add_employee.html", context)


def view_users(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorised access!")
    context = dict()
    context["title"] = "View Users | Admin"
    context['heading'] = "User Details Page"
    if if_admin(request):
        role = 0
    elif if_manager(request):
        role = 1
    elif if_hr(request):
        role = 2
    else:
        return HttpResponse("Unauthorised access!")
    context['role'] = role
    data = list()
    for manager in Manager.objects.all():
        data.append((manager, Employee.objects.all().filter(my_manager=manager)))
    context['data'] = data
    return render(request, "admin/view_users.html", context)

def view_user_details(request, pk):
    try:
        user = User.objects.all().get(id=pk)
        user.to
        print(user)
    except Exception as e:
        print(e)  # meant for debugging purposes
        messages.error(request, "Something went wrong! User not found.")

    return render(request, "admin/view_user.html")
