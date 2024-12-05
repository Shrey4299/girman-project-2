"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = [
        'email', 'name', 'phone_number', 'is_active',
        'is_staff', 'registered', 'image_uploaded', 'experience', 'role'
    ]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'phone_number', 'experience', 'role')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Other Info'), {'fields': ('registered', 'image_uploaded')}),
    )

    readonly_fields = ['last_login']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'phone_number',
                'experience',
                'role',  # Including role field during user creation
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    """Define the admin pages for roles."""
    list_display = ('role_name',)  # Display role_name as the main field
    search_fields = ('role_name',)  # Add search functionality for role_name
    list_filter = ('role_name',)  # Add filter for role_name
    filter_horizontal = ('permissions',)  # Add a horizontal filter for permissions

@admin.register(models.Permission)
class PermissionAdmin(admin.ModelAdmin):
    """Define the admin pages for permissions."""
    list_display = ('method', 'name', 'url', 'description')  # Display method, name, URL, and description
    search_fields = ('name', 'url')  # Add search functionality for permissions
    list_filter = ('method',)  # Add filter for HTTP methods


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'isbn', 'pages', 'language')
    search_fields = ('title', 'author', 'isbn')  # Search functionality by title, author, and ISBN
    list_filter = ('language', 'published_date')  # Filter by language and published date
# Register the User model with the custom admin class
admin.site.register(models.User, UserAdmin)
