from rest_framework import viewsets
from helper import HasRolePermission, IsAdminRole
from core.models import Permission
from user.serializers import PermissionSerializer
from rest_framework import authentication


class PermissionViewSet(viewsets.ModelViewSet):
    """ViewSet for the Permission model."""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [HasRolePermission] 
