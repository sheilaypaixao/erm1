from companies.views.base import Base
from companies.utils.permissions import GroupingPermissions
from django.contrib.auth.models import Permission

from companies.serializers import PermissionsSerializer

from rest_framework.views import Response

class Permissions(Base):
    permission_classes = [GroupingPermissions]

    def get(self, request):
        permissions = Permission.objects.filter(content_type_id__in=[7,10,12]).all()

        serializers = PermissionsSerializer(permissions, many=True)

        return Response({"permissions": serializers.data})