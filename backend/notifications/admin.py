from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'is_deleted', 'created_at']
    search_fields = ['title', 'message', 'user__full_name', 'user__email']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('user', 'sender', 'notification_type')}),
        ('Content', {'fields': ('title', 'message')}),
        ('Status', {'fields': ('is_read', 'is_deleted')}),
        ('References', {'fields': ('connection',)}),
        ('Timestamps', {'fields': ('created_at', 'read_at')}),
    )
    
    readonly_fields = ['created_at', 'read_at']
