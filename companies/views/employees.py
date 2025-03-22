from companies.views.base import Base
from companies.utils.permissions import EmployeePermissions
from rest_framework.exceptions import APIException

from companies.models import Employee, Enterprise
from accounts.models import User
from accounts.auth import Authentication
from companies.serializers import EmployeeSerializers, EmployeeDetailSerializers

from rest_framework.views import Response

class Employees(Base):
    permission_classes = [EmployeePermissions]

    def get(self, request):
        with_owner = request.GET.get("with_owner", False)

        enterprise_id = self.get_enterprise_id(request.user.id)
        owner_id = Enterprise.objects.filter(id=enterprise_id).first().owner_id

        employees = Employee.objects.filter(enterprise_id=enterprise_id).all()

        print(with_owner)

        if not with_owner or with_owner == "false":
            employees = employees.exclude(user_id=owner_id).all()

        serializer = EmployeeSerializers(employees, many=True)

        return Response({"employees": serializer.data})

    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        password = request.data.get("password")
        group_id = request.data.get("group_id")

        enterprise_id = self.get_enterprise_id(request.user.id)

        user = Authentication.signup(self, name=name, email=email, password=password, type_account="employee", company_id=enterprise_id)
        group = self.get_grouping(group_id, enterprise_id)
        user.grouping = group
        user.save()

        employee = Employee.objects.get(user_id=user.id)
        serializer = EmployeeDetailSerializers(employee)

        return Response({"employee": serializer.data})

class EmployeesDetail(Base):

    def get(self, request, employee_id):
        employee = self.get_employee(employee_id, request.user.id)

        serializer = EmployeeDetailSerializers(employee)

        return Response({"employee": serializer.data})

    def put(self, request, employee_id):
        group_id = request.data.get("group_id")
        employee = self.get_employee(employee_id, request.user.id)
        enterprise_id = self.get_enterprise_id(request.user.id)
        
        name = request.data.get("name") or employee.user.name
        email = request.data.get("email") or employee.user.email

        if email!=employee.user.email and User.objects.filter(email=email).exists():
            raise APIException("Esse email já está em uso")
        
        group = self.get_grouping(group_id, enterprise_id)

        employee.user.grouping = group
        employee.user.name = name
        employee.user.email = email
        employee.user.save()

        return Response({"success": True})

    def delete(self, request, employee_id):
        employee = self.get_employee(employee_id, request.user.id)
        user = User.objects.filter(id=employee.user.id).first()

        if user.is_owner == 1:
            raise APIException("Dono da empresa não pode ser demitido!")

        employee.delete()
        user.delete()

        return Response({"success": True})








