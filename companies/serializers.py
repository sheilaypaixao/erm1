from rest_framework import serializers

from accounts.models import User, Grouping, Grouping_Permissions
from companies.models import Employee, Task, TaskStatus

from django.contrib.auth.models import Permission

class EmployeeSerializers(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = (
            "id",
            "name",
            "email"
        )
    
    def get_name(self, obj):
        return obj.user.name
    
    def get_email(self,obj):
        return obj.user.email
    
class EmployeeDetailSerializers(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            "id",
            "name",
            "email",
            "group"
        )
    
    def get_name(self, obj):
        return obj.user.name
    
    def get_email(self,obj):
        return obj.user.email
    
    def get_group(self,obj):
        return GroupingSerializer(obj.user.grouping).data
    

class GroupingSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Grouping
        fields=(
            "id",
            "name",
            "permissions"
        )
    
    def get_permissions(self, obj):
        permissions = obj.permissions.all()
        permissionsData = []

        for permission in permissions:
            permissionsData.append({
                "id": permission.id,
                "name": permission.name,
                "codename": permission.codename
            })
        
        return permissionsData

class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields=(
            "id",
            "name",
            "codename"
        )

class TasksSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()
    creator_employee = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields=(
            "id",
            "title",
            "description",
            "due_date",
            "created_at",
            "updated_at",
            "status",
            "employee",
            "creator_employee"
        )
    
    def get_status(self, obj):
        return TaskStatusSerializer(obj.status).data
    
    def get_employee(self, obj):
        return EmployeeDetailSerializers(obj.employee).data

    def get_creator_employee(self, obj):
        return EmployeeDetailSerializers(obj.creator_employee).data

class TaskSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()
    creator_employee = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields=(
            "id",
            "title",
            "description",
            "due_date",
            "created_at",
            "updated_at",
            "status",
            "employee",
            "creator_employee"
        )
    
    def get_status(self, obj):
        return TaskStatusSerializer(obj.status).data
    
    def get_employee(self, obj):
        return EmployeeDetailSerializers(obj.employee).data

    def get_creator_employee(self, obj):
        return EmployeeDetailSerializers(obj.creator_employee).data

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.status_id = validated_data.get("status_id", instance.status_id)
        instance.employee_id = validated_data.get("employee_id", instance.employee_id)
        instance.duo_data = validated_data.get("duo_data", instance.duo_data)
    
        instance.save()

        return instance

class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields=(
            "id",
            "name",
            "codename",
        )