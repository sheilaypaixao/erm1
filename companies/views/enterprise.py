from companies.views.base import Base
from accounts.auth import Authentication
from accounts.serializers import UserSerializer
from rest_framework.views import Response

class Enterprise(Base):
    def post(self, request):
        name = request.get("name")
        email = request.get("email")
        password = request.get("password")
        enterprise_name = request.get("enterprise_name")

        user = Authentication.signup(self, name, email, password, "owner", enterprise_name)

        serializer = UserSerializer(user)

        return Response({"user": serializer.data})

