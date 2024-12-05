from rest_framework import viewsets
from helper import HasRolePermission, IsAdminRole
from core.models import Role
from user.serializers import RoleSerializer
from rest_framework import authentication


class RoleViewSet(viewsets.ModelViewSet):
    """ViewSet for the Role model."""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    authentication_classes = [authentication.TokenAuthentication]