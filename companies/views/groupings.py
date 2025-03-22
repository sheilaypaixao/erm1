from companies.views.base import Base
from accounts.models import Grouping, Grouping_Permissions
from django.contrib.auth.models import Permission
from companies.serializers import GroupingSerializer
from companies.utils.permissions import GroupingPermissions
from companies.utils.exceptions import RequiredFields

from rest_framework.views import Response
from rest_framework.exceptions import APIException

class Groupings(Base):
    permission_classes = [GroupingPermissions]

    def get(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id)
        
        groups = Grouping.objects.filter(enterprise_id=enterprise_id).all()

        serializer = GroupingSerializer(groups, many=True)

        return Response({"groups": serializer.data})

    def post(self, request):
        name = request.data.get("name")
        permissions = request.data.get("permissions")

        enterprise_id = self.get_enterprise_id(request.user.id)

        if not name:
            raise RequiredFields
        
        created_group = Grouping.objects.create(
            name = name,
            enterprise_id=enterprise_id
        )

        self.add_permissions_to_group(created_group, permissions)
        
        serializer = GroupingSerializer(created_group)

        return Response({"group": serializer.data })

class GroupingDetail(Base):
    def get(self, request, grouping_id):
        enterprise_id = self.get_enterprise_id(request.user.id)
        grouping = self.get_grouping(grouping_id, enterprise_id)

        serializer = GroupingSerializer(grouping)

        return Response({"group": serializer.data })

    def put(self, request, grouping_id):
        enterprise_id = self.get_enterprise_id(request.user.id)
        grouping = self.get_grouping(grouping_id, enterprise_id)

        name = request.data.get("name") or grouping.name
        permissions = request.data.get("permissions")

        grouping.name = name
        grouping.save()

        Grouping_Permissions.objects.filter(grouping_id=grouping_id).delete()
        self.add_permissions_to_group(grouping, permissions)

        return Response({"success": True })

    def delete(self, request, grouping_id):
        enterprise_id = self.get_enterprise_id(request.user.id)
        grouping = self.get_grouping(grouping_id, enterprise_id)

        try:
            grouping.delete()
        except ValueError:
            raise APIException("Não foi possível deletar o cargo, há funcionários associados a ele.")

        return Response({"success": True })




    
