from companies.views.base import Base
from companies.models import Task, TaskStatus
from companies.serializers import TasksSerializer, TaskSerializer
from companies.utils.permissions import TaskPermissions

from rest_framework.views import Response
from rest_framework.exceptions import APIException
import datetime

class Tasks(Base):
    permission_classes = [TaskPermissions]

    def get(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)
        tasks = Task.objects.filter(enterprise_id=enterprise_id, employee_id=request.user.id)

        serializer = TasksSerializer(tasks, many=True)

        return Response({"tasks": serializer.data})

    def post(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)
        
        title = request.data.get("title")
        description = request.data.get("description")
        due_date = request.data.get("due_date")
        status_id = request.data.get("status_id")
        employee_id = request.data.get("employee_id")

        employee = self.get_employee(employee_id, request.user.id)
        employee_creator = self.get_employee(request.user.id, request.user.id)
        status = self.get_status(status_id)

        if not title or len(title) > 125:
            raise APIException("Envie o título no formato correto")

        if due_date:
            due_date = self.verify_date(due_date)

        created_task = Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            enterprise_id=enterprise_id,
            employee=employee,
            status=status,
            creator_employee = employee_creator
        )

        serializer = TaskSerializer(created_task)

        return Response({"task": serializer.data})

class TaskDetail(Base):
    permission_classes = [TaskPermissions]

    def get(self, request, task_id):
        enterprise_id = self.get_enterprise_id(request.user.id)

        task = self.get_task(task_id, enterprise_id)

        serializer = TaskSerializer(task)

        return Response({"task": serializer.data})

    def put(self, request, task_id):
        enterprise_id = self.get_enterprise_id(request.user.id)
        task = self.get_task(task_id, enterprise_id)

        title = request.data.get("title", task.title)
        description = request.data.get("description", task.description)
        due_date = request.data.get("due_date", task.due_date)
        status_id = request.data.get("status_id", task.status_id)
        employee_id = request.data.get("employee_id", task.employee_id)

        if not title or len(title) > 125:
            raise APIException("Envie o título no formato correto")
        
        if due_date and due_date!= task.due_date:
            due_date = self.verify_date(due_date)

        employee = self.get_employee(employee_id, request.user.id)
        status = self.get_status(status_id)

        task.title = title
        task.description = description
        task.due_date = due_date
        task.employee = employee
        task.status = status

        task.save()

        serializer = TaskSerializer(task)

        return Response({"task": serializer.data})

    def delete(self, request, task_id):
        enterprise_id = self.get_enterprise_id(request.user.id)
        task = self.get_task(task_id, enterprise_id)

        task.delete()

        return Response({"success": True})


class TasksCreated(Base):
    def get(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)
        tasks = Task.objects.filter(enterprise_id=enterprise_id, creator_employee_id=request.user.id)

        serializer = TasksSerializer(tasks, many=True)

        return Response({"tasks": serializer.data})