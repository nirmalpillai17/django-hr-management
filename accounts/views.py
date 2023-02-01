from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from .forms import *


def admin_signup(request):
    context = dict()
    context['title'] = "Admin | Sign Up"
    context['heading'] = "Admin User Sign Up"
    form = AdminSignUp(request.POST or None)
    context['form'] = form
    if request.method == "POST":
        if form.is_valid():
            fs = form.save(commit = False)
            fs.first_name = form.cleaned_data["first_name"].title()
            fs.last_name = form.cleaned_data["last_name"].title()
            fs.emp_id = form.cleaned_data["emp_id"].upper()
            fs.save()
            return redirect("admin_login")
        return redirect("admin_signup")
    return render(request, "accounts/signup.html", context)

def manager_signup(request):
    return HttpResponse("success")


def hr_signup(request):
    return HttpResponse("success")


def admin_login(request):
    return HttpResponse("success")


def manager_login(request):
    return HttpResponse("success")


def hr_login(request):
    return HttpResponse("success")


def employee_login(request):
    return HttpResponse("success")

def home_view(request):
    return render(request, "accounts/home.html")
