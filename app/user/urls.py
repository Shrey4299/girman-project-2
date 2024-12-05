from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views.books_view import BookViewSet
from user.views.permissions_view import PermissionViewSet
from user.views.roles_view import RoleViewSet
from user.views.users_view import CreateTokenView, CreateUserView, ManageUserView

app_name = 'user'

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'books', BookViewSet)  # Register the Book viewset
router.register(r'roles', RoleViewSet)  # Register the Role viewset
router.register(r'permissions', PermissionViewSet)  # Register the Permission viewset

urlpatterns = [
    # User-related URLs
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me'),

    # Book, Role, and Permission API URLs
    path('', include(router.urls)),  # Include all viewsets (Book, Role, Permission)
]
