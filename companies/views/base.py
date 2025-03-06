from rest_framework.views import APIView

from companies.utils.exceptions import NotFoundEmployee, NotFoundGroup, RequiredFields, NotFoundTaskStatus, NotFoundTask
from companies.models import Employee, Enterprise, Task, TaskStatus

from accounts.models import Grouping

class Base(APIView):
    def get_enterprise_id(self, user_id):

        employee = Employee.objects.filter(user_id=user_id).first()
        owner = Enterprise.objects.filter(owner_id=user_id).first()

        if employee:
            return employee.enterprise.id
        elif owner:
            return owner.id

    def get_employee(self, employee_id, user_id):
        enterprise_id = self.get_enterprise_id(user_id)

        employee = Employee.objects.filter(id=employee_id, enterprise_id=enterprise_id).first()
        
        if not employee:
            raise NotFoundEmployee
        
        return employee
    
    def get_grouping(self, grouping_id, enterprise_id):
        
        grouping = Grouping.objects.filter(id=grouping_id, enterprise_id=enterprise_id).first()

        if not grouping:
            raise NotFoundGroup
        
        return grouping
    
    def get_status(self, status_id):

        status = TaskStatus.objects.filter(id=status_id).first()

        if not status:
            raise NotFoundTaskStatus
        
        return status
    
    def get_tasks(self, tasks_id, enterprise_id):
        task = Task.objects.filter(id=tasks_id, enterprise_id=enterprise_id).first()

        if not task:
            raise NotFoundTask

        return task
