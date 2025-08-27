from rest_framework import serializers
from .models import Notification
from users.serializers import UserSearchSerializer

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications"""
    sender = UserSearchSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'title', 'message', 
            'sender', 'is_read', 'created_at', 'read_at'
        ]
        read_only_fields = ['id', 'created_at', 'read_at']

class NotificationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating notifications"""
    
    class Meta:
        model = Notification
        fields = ['notification_type', 'title', 'message', 'user']

class NotificationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating notification status"""
    
    class Meta:
        model = Notification
        fields = ['is_read']
