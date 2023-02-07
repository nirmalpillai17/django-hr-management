from django.urls import path

from . import views

urlpatterns = [
    path("home_admin", views.admin_home, name="admin_home"),
    path("home_manager", views.manager_home, name="manager_home"),
    path("home_hr", views.hr_home, name="hr_home"),
    path("home_employee", views.employee_home, name="employee_home"),
    
    path("add_employee", views.add_employee, name="add_employee"),
    path("create_user", views.user_creation, name="create_user"),
    path("handle_request/<int:pk>", views.handle_request, name="handle_request"),
    path("dismiss_request/<int:pk>", views.dismiss_request, name="dismiss_request"),

    path("view_users", views.view_users, name="view_users"),
    path("view_user/<int:pk>", views.view_user_details, name="view_user"),
]
