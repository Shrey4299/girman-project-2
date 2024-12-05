import re
from rest_framework import permissions
from core.models import Role, Permission

class HasRolePermission(permissions.BasePermission):
    """
    Custom permission to only allow access to users with a role that has specific permissions.
    """
    def has_permission(self, request, view):
        # Get the user from the request
        user = request.user

        print(request)

        if not user.is_authenticated:
            print("User is not authenticated")
            return False

        # Check if the user has a role
        if not hasattr(user, 'role') or not user.role:
            print("User does not have a role")
            return False

        # Determine the HTTP method
        method = request.method  # e.g., 'GET', 'POST', 'DELETE'
        print(f"HTTP Method: {method}")

        # Normalize the URL to replace dynamic segments with placeholders
        raw_url = request.path
        normalized_url = re.sub(r'/\d+/', '/{id}/', raw_url)
        print(f"Normalized URL: {normalized_url}")

        # Fetch the user's role
        print(f"Fetching user {user}")
        try:
            role = Role.objects.get(role_name=user.role.role_name)
            print(f"User's Role: {role}")
        except Role.DoesNotExist:
            print("Role does not exist")
            return False

        if role == "ADMIN":
            return True

        # Check if the role has a permission matching the method and normalized URL
        try:
            permission = Permission.objects.get(method=method, url=normalized_url)
            print(f"Required Permission: {permission}")
        except Permission.DoesNotExist:
            print("No matching permission found")
            return False

        # Check if the role has the permission
        if permission not in role.permissions.all():
            print("Role does not have the required permission")
            return False

        print("Permission granted")
        return True


class IsAdminRole(permissions.BasePermission):
    """
    Custom permission to grant access only to users with the ADMIN role.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        user = request.user
        role = Role.objects.get(role_name=user.role.role_name)
        print(f"User's Role: {role}")

        # Check if the user has a role and that role is ADMIN
        if hasattr(request.user, 'role') and request.user.role.role_name == 'ADMIN':
            print(request.user.role.role_name)
            print(request.user)
            print("Permission granted")
            return True

        return False