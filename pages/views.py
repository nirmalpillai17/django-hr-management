from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib import messages

from accounts.models import *
from .forms import *

ADD_EMP_DONE = "Add employee request sent successfully."


def admin_home(request):
    if request.user.is_authenticated:
        context = dict()
        context["title"] = "Home | Admin"
        context["heading"] = "Admin Home Page"
        username = request.user.username
        user = Admin.objects.all().get(username=username)
        context["user"] = user
        return render(request, "pages/admin_home.html", context)
    else:
        return HttpResponse("Unauthorised access!")


def manager_home(request):
    if request.user.is_authenticated:
        context = dict()
        context["title"] = "Home | Manager"
        context["heading"] = "Manager Home Page"
        username = request.user.username
        user = Manager.objects.all().get(username=username)
        context["user"] = user
        return render(request, "pages/manager_home.html", context)
    else:
        return HttpResponse("Unauthorised access!")


def hr_home(request):
    if request.user.is_authenticated:
        context = dict()
        context["title"] = "Home | HR"
        context["heading"] = "HR Home Page"
        username = request.user.username
        user = HRManager.objects.all().get(username=username)
        context["user"] = user
        return render(request, "pages/hr_home.html", context)
    else:
        return HttpResponse("Unauthorised access!")


def employee_home(request):
    if request.user.is_authenticated:
        context = dict()
        context["title"] = "Home | Employee"
        context["heading"] = "Employee Home Page"
        username = request.user.username
        user = Employee.objects.all().get(username=username)
        context["user"] = user
        return render(request, "pages/employee_home.html", context)
    else:
        return HttpResponse("Unauthorised access!")


def user_creation(request):  # function for admins
    context = dict()
    context["title"] = "Create User | Admin"
    context["heading"] = "Create User Requests"
    context["requests"] = NewEmployees.objects.all()
    if request.method == "POST":
        return redirect("admin_home")
    return render(request, "create_user.html", context)


def add_employee(request):  # function for manager
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
                form.cleaned_data["last_name"].title()
            fs.save()
            messages.success(request, ADD_EMP_DONE)
            return redirect("hr_home")
        for error_list in form.errors.values():
            for error in error_list:
                messages.warning(request, error)
            return redirect("add_employee")
    return render(request, "hr/add_employee.html", context)
