from accounts.models import *


def if_admin(request):
    if request.user.is_authenticated:
        username = request.user.username
        if Admin.objects.all().filter(username=username).exists():
            return True
    return False


def if_manager(request):
    if request.user.is_authenticated:
        username = request.user.username
        if Manager.objects.all().filter(username=username).exists():
            return True
    return False


def if_hr(request):
    if request.user.is_authenticated:
        username = request.user.username
        if HRManager.objects.all().filter(username=username).exists():
            return True
    return False


def if_employee(request):
    if request.user.is_authenticated:
        username = request.user.username
        if Employee.objects.all().filter(username=username).exists():
            return True
    return False
