from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("signup_admin", views.admin_signup, name="admin_signup"),
    path("signup_manager", views.manager_signup, name="manager_signup"),
    path("signup_hr", views.hr_signup, name="hr_signup"),
    #path("signup_employee", views.employee_signup, name="employee_signup"),

    path("login_admin", views.admin_login, name="admin_login"),
    path("login_manager", views.manager_login, name="manager_login"),
    path("login_hr", views.hr_login, name="hr_login"),
    path("login_employee", views.employee_login, name="employee_login"),
]