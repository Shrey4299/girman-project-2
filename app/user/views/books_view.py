from rest_framework import viewsets
from helper import HasRolePermission
from core.models import Book
from user.serializers import BookSerializer
from rest_framework import authentication

class BookViewSet(viewsets.ModelViewSet):
    """ViewSet for the Book model."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [HasRolePermission]  # Apply the custom permission class
