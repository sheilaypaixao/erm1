from django.urls import path, include
from companies.views.employees import Employees, EmployeesDetail
from companies.views.permissions import Permissions
from companies.views.groupings import Groupings, GroupingDetail
from companies.views.tasks import Tasks, TaskDetail, TasksCreated, TaskStatusDetail

urlpatterns = [
    path("employees", Employees.as_view()),
    path("employees/<int:employee_id>", EmployeesDetail.as_view()),
    
    path("permissions", Permissions.as_view()),

    path("groups", Groupings.as_view()),
    path("groups/<int:grouping_id>", GroupingDetail.as_view()),

    path("tasks", Tasks.as_view()),
    path("tasks/<int:task_id>", TaskDetail.as_view()),
    path("tasks/created", TasksCreated.as_view()),
    path("tasks/status", TaskStatusDetail.as_view())
]