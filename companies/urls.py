from django.urls import path, include
from companies.views.employees import Employees, EmployeesDetail
from companies.views.permissions import Permissions

urlpatterns = [
    path("employees", Employees.as_view()),
    path("employees/<int:employee_id>", EmployeesDetail.as_view()),
    
    path("permissions", Permissions.as_view()),
]