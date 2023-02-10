from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib import messages
import string
import random

from accounts.models import *
from .forms import *

from accounts.custom import *

ADD_EMP_DONE = "Add employee request sent successfully."
USER_CREATION_DONE = "User for employee created successfully."
USER_CREATION_FAIL = "Sorry! An unexpected error occured. Please try again."
USER_NF = "Something went wrong! User not found."


def admin_home(request):
    if not if_admin(request):
        return redirect("admin_login")

    context = dict()
    context["title"] = "Home | Admin"
    context["heading"] = "Admin Home Page"
    username = request.user.username
    user = Admin.objects.all().get(username=username)
    context["user"] = user
    return render(request, "pages/admin_home.html", context)


def manager_home(request):
    if not if_manager(request):
        return redirect("manager_login")

    context = dict()
    context["title"] = "Home | Manager"
    context["heading"] = "Manager Home Page"
    username = request.user.username
    user = Manager.objects.all().get(username=username)
    context["user"] = user
    return render(request, "pages/manager_home.html", context)


def hr_home(request):
    if not if_hr(request):
        return redirect("hr_login")

    context = dict()
    context["title"] = "Home | HR"
    context["heading"] = "HR Home Page"
    username = request.user.username
    user = HRManager.objects.all().get(username=username)
    context["user"] = user
    return render(request, "pages/hr_home.html", context)


def employee_home(request):
    if not if_employee(request):
        return redirect("employee_login")

    context = dict()
    context["title"] = "Home | Employee"
    context["heading"] = "Employee Home Page"
    username = request.user.username
    user = Employee.objects.all().get(username=username)
    context["user"] = user
    return render(request, "pages/employee_home.html", context)


def user_creation(request):  # function for admins
    if not if_admin(request):
        return redirect("admin_login")

    context = dict()
    context["title"] = "Create User | Admin"
    context["heading"] = "Create User Requests"
    context["requests"] = NewEmployees.objects.all()
    return render(request, "admin/create_user.html", context)


def handle_request(request, pk):
    if not if_admin(request):
        return redirect("admin_login")

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

    try:
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
            my_hr = user.my_hr,
        )
        user.delete()
        messages.success(request, USER_CREATION_DONE)
    except:
        messages.error(request, USER_CREATION_FAIL)

    return redirect("create_user")


def dismiss_request(request, pk):
    if not if_admin(request):
        return redirect("admin_login")

    # skipping validation, to be added later
    user = NewEmployees.objects.all().get(id=pk)
    user.delete()
    return redirect("create_user")


def add_employee(request):  # function for hr
    if not if_hr(request):
        return redirect("hr_login")

    context = dict()
    context["title"] = "New Employee | HR"
    context["heading"] = "Add Employee Page"
    form = EditEmployeeDetails(request.POST or None)
    context["form"] = form
    if request.method == "POST":
        if form.is_valid():
            fs = form.save(commit=False)
            fs.first_name = form.cleaned_data["first_name"].title()
            fs.last_name = form.cleaned_data["last_name"].title()
            fs.my_hr_id = request.user.id
            fs.save()
            messages.success(request, ADD_EMP_DONE)
            return redirect("hr_home")

        # the following error handling is optional
        for error_list in form.errors.values():
            for error in error_list:
                messages.warning(request, error)
        # end of error handling

        return redirect("add_employee")
    return render(request, "hr/add_employee.html", context)


def view_users(request):
    if if_admin(request):
        role = 0
        managers = Manager.objects.all()
    elif if_manager(request):
        role = 1
        managers = Manager.objects.filter(username=request.user.username)
    elif if_hr(request):
        role = 2
        managers = Manager.objects.all()
    else:
        return redirect("/accounts/")

    context = dict()
    context["title"] = "View Users | Admin"
    context["heading"] = "User Details Page"
    context["role"] = role
    data = list()
    for manager in managers:
        data.append((manager, Employee.objects.all().filter(my_manager=manager)))
    context["data"] = data
    return render(request, "admin/view_users.html", context)


def view_admin_details(request, pk):
    if not if_admin(request):
        return redirect("admin_login")

    context = dict()
    context["title"] = "View Details | Admin"
    context["heading"] = "Admin Details Page"
    try:
        user = Admin.objects.all().get(id=pk)
        if request.user.id != pk:
            raise Exception()
        hr_count = HRManager.objects.all().filter(my_admin=user).count
        manager_count = Manager.objects.all().filter(my_admin=user).count
        data = (
            ("Username", user.username),
            ("First Name", user.first_name),
            ("Last Name", user.last_name),
            ("Email", user.email),
            ("Mobile No.", user.mobile),
            ("Organization", user.org),
            ("Employee ID", user.emp_id),
            ("HR Count", hr_count),
            ("Manager Count", manager_count),
        )
        context["data"] = data
    except:
        messages.error(request, USER_NF)
    return render(request, "admin/view_user.html", context)


def view_manager_details(request, pk):
    if not (if_admin(request) or if_manager(request)):
        return redirect("manager_login")

    context = dict()
    context["title"] = "View Details | Manager"
    context["heading"] = "Manager Details Page"
    try:
        user = Manager.objects.all().get(id=pk)
        cur_id = request.user.id
        if (cur_id != user.my_admin.id) and (cur_id != user.id):
            raise Exception()
        employee_count = Employee.objects.all().filter(my_manager=user).count
        data = (
            ("Username", user.username),
            ("First Name", user.first_name),
            ("Last Name", user.last_name),
            ("Email", user.email),
            ("Mobile No.", user.mobile),
            # ("Gender", user.gender),
            # ("Date of Birth", user.dob),
            ("Organization", user.my_admin.org),
            ("Employee ID", user.emp_id),
            ("Employee Count", employee_count),
        )
        context["data"] = data
    except:
        messages.error(request, USER_NF)
    return render(request, "admin/view_user.html", context)


def view_hr_details(request, pk):
    if not (if_admin(request) or if_hr(request)):
        return redirect("manager_login")

    context = dict()
    context["title"] = "View Details | HR"
    context["heading"] = "HR Details Page"
    try:
        user = HRManager.objects.all().get(id=pk)
        cur_id = request.user.id
        if (cur_id != user.my_admin.id) and (cur_id != user.id):
            raise Exception()
        employee_count = Employee.objects.all().filter(my_hr=user).count
        data = (
            ("Username", user.username),
            ("First Name", user.first_name),
            ("Last Name", user.last_name),
            ("Email", user.email),
            ("Mobile No.", user.mobile),
            # ("Gender", user.gender),
            # ("Date of Birth", user.dob),
            ("Organization", user.my_admin.org),
            ("Employee ID", user.emp_id),
            ("Employee Count", employee_count),
        )
        context["data"] = data
    except:
        messages.error(request, USER_NF)
    return render(request, "admin/view_user.html", context)


def view_employee_details(request, pk):
    context = dict()
    context["title"] = "View Details | Employee"
    context["heading"] = "Employee Details Page"
    if not request.user.is_authenticated:
        return redirect("/accounts/")
    try:
        user = Employee.objects.all().get(id=pk)
        cur_id = request.user.id
        conditions = (
            cur_id != user.id,
            cur_id != user.my_manager.id,
            cur_id != user.my_hr.id,
            cur_id != user.my_manager.my_admin.id,
        )
        if all(conditions):
            raise Exception()
        data = (
            ("Username", user.username),
            ("First Name", user.first_name),
            ("Last Name", user.last_name),
            ("Email", user.email),
            ("Mobile No.", user.mobile),
            ("Gender", user.gender),
            ("Date Of Birth", user.dob),
            ("Organization", user.my_manager.my_admin.org),
            ("Manager", user.my_manager.first_name),
            ("HR Manager", user.my_hr.first_name),
            ("Start Date", user.start_date),
            ("Quit Date", user.quit_date),
            ("Employee ID", user.emp_id),
        )
        context["data"] = data
    except:
        messages.error(request, USER_NF)
    return render(request, "admin/view_user.html", context)


# to be reviewd
def view_profile(request):
    if if_admin(request):
        return redirect("view_admin", pk=request.user.pk)
    elif if_manager(request):
        return redirect("view_manager", pk=request.user.pk)
    elif if_hr(request):
        return redirect("view_hr", pk=request.user.pk)
    else:
        return redirect()  # changes to be made
