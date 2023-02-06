from django.urls import path

from . import views

urlpatterns = [
    path("home_admin", views.admin_home, name="admin_home"),
    path("home_manager", views.manager_home, name="manager_home"),
    path("home_hr", views.hr_home, name="hr_home"),
    path("home_employee", views.employee_home, name="employee_home"),
]
