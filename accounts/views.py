from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from .forms import *
from .models import *


USER_TYPE_ERR = "User is not an {}. Please use correct login page."
USER_INCORRECT = "Username or password is incorrect."


def admin_signup(request):
    context = dict()
    context["title"] = "Sign Up | Admin"
    context["heading"] = "Admin User Sign Up"
    form = AdminSignUp(request.POST or None)
    context["form"] = form
    if request.method == "POST":
        if form.is_valid():
            fs = form.save(commit=False)
            fs.first_name = form.cleaned_data["first_name"].title()
            fs.last_name = form.cleaned_data["last_name"].title()
            fs.emp_id = form.cleaned_data["emp_id"].upper()
            fs.save()
            return redirect("admin_login")
        for error_list in form.errors.values():
            for error in error_list:
                messages.warning(request, error)
        return redirect("admin_signup")
    return render(request, "accounts/signup.html", context)


def manager_signup(request):
    context = dict()
    context["title"] = "Sign Up | Manager"
    context["heading"] = "Manager User Sign Up"
    form = ManagerSignUp(request.POST or None)
    context["form"] = form
    if request.method == "POST":
        if form.is_valid():
            fs = form.save(commit=False)
            fs.first_name = form.cleaned_data["first_name"].title()
            fs.last_name = form.cleaned_data["last_name"].title()
            fs.emp_id = form.cleaned_data["emp_id"].upper()
            fs.save()
            return redirect("manager_login")
        for error_list in form.errors.values():
            for error in error_list:
                messages.warning(request, error)
        return redirect("manager_signup")
    return render(request, "accounts/signup.html", context)


def hr_signup(request):
    context = dict()
    context["title"] = "Sign Up | HR"
    context["heading"] = "HR User Sign Up"
    form = HRSignUp(request.POST or None)
    context["form"] = form
    if request.method == "POST":
        if form.is_valid():
            fs = form.save(commit=False)
            fs.first_name = form.cleaned_data["first_name"].title()
            fs.last_name = form.cleaned_data["last_name"].title()
            fs.emp_id = form.cleaned_data["emp_id"].upper()
            fs.save()
            return redirect("hr_login")
        for error_list in form.errors.values():
            for error in error_list:
                messages.warning(request, error)
        return redirect("hr_signup")
    return render(request, "accounts/signup.html", context)


def admin_login(request):
    context = dict()
    context["title"] = "Log In | Admin"
    context["heading"] = "Admin User Log In"
    form = LoginForm(request.POST or None)
    context["form"] = form
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if Admin.objects.all().filter(username=user.username).exists():
                    login(request, user)
                    return redirect("admin_home")
                messages.warning(request, USER_TYPE_ERR.format("Admin"))
            else:
                messages.warning(request, USER_INCORRECT)
        return redirect("admin_login")
    return render(request, "accounts/login.html", context)


def manager_login(request):
    context = dict()
    context["title"] = "Log In | Manager"
    context["heading"] = "Manager User Log In"
    form = LoginForm(request.POST or None)
    context["form"] = form
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if Manager.objects.all().filter(username=user.username).exists():
                    login(request, user)
                    return redirect("manager_home")
                messages.warning(request, USER_TYPE_ERR.format("Manager"))
            else:
                messages.warning(request, USER_INCORRECT)
        return redirect("manager_login")
    return render(request, "accounts/login.html", context)


def hr_login(request):
    context = dict()
    context["title"] = "Log In | HR"
    context["heading"] = "HR User Log In"
    form = LoginForm(request.POST or None)
    context["form"] = form
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if HRManager.objects.all().filter(username=user.username).exists():
                    login(request, user)
                    return redirect("hr_home")
                messages.warning(request, USER_TYPE_ERR.format("HR"))
            else:
                messages.warning(request, USER_INCORRECT)
        return redirect("hr_login")
    return render(request, "accounts/login.html", context)


def employee_login(request):
    context = dict()
    context["title"] = "Log In | Employee"
    context["heading"] = "Employee User Log In"
    form = LoginForm(request.POST or None)
    context["form"] = form
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if HRManager.objects.all().filter(username=user.username).exists():
                    login(request, user)
                    return redirect("employee_home")
                messages.warning(request, USER_TYPE_ERR.format("Employee"))
            else:
                messages.warning(request, USER_INCORRECT)
        return redirect("employee_login")
    return render(request, "accounts/login.html", context)


def home_view(request):
    return render(request, "accounts/home.html")


def logout_view(request):
    logout(request)
    return redirect("/accounts/")
