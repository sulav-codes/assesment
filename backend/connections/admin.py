from django.contrib import admin
from .models import Connection

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['sender__full_name', 'receiver__full_name', 'sender__email', 'receiver__email']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('sender', 'receiver', 'status')}),
        ('Message', {'fields': ('message',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    
    readonly_fields = ['created_at', 'updated_at']
