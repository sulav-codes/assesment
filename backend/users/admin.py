from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['user_id', 'full_name', 'email', 'company', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'industry', 'date_joined']
    search_fields = ['full_name', 'email', 'user_id', 'company']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'contact', 'user_id')}),
        ('Professional info', {'fields': ('company', 'industry', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'contact', 'company', 'industry', 'address', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['user_id', 'date_joined', 'last_login']
