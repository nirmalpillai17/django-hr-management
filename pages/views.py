from django.shortcuts import render
from django.shortcuts import HttpResponse

from accounts.models import *


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
