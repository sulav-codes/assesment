from rest_framework import serializers
from django.db import models
from .models import Connection
from users.serializers import UserSearchSerializer

class ConnectionRequestSerializer(serializers.ModelSerializer):
    """Serializer for creating connection requests"""
    
    class Meta:
        model = Connection
        fields = ['receiver', 'message']
    
    def validate_receiver(self, value):
        """Ensure user cannot send request to themselves"""
        request = self.context.get('request')
        if request and request.user == value:
            raise serializers.ValidationError("You cannot send a connection request to yourself.")
        return value
    
    def validate(self, attrs):
        """Check if connection already exists"""
        request = self.context.get('request')
        receiver = attrs.get('receiver')
        
        if request:
            # Check if connection already exists in either direction
            existing_connection = Connection.objects.filter(
                models.Q(sender=request.user, receiver=receiver) |
                models.Q(sender=receiver, receiver=request.user)
            ).first()
            
            if existing_connection:
                raise serializers.ValidationError("Connection already exists between these users.")
        
        return attrs
    
    def create(self, validated_data):
        """Create connection request"""
        request = self.context.get('request')
        validated_data['sender'] = request.user
        return super().create(validated_data)

class ConnectionResponseSerializer(serializers.Serializer):
    """Serializer for responding to connection requests"""
    action = serializers.ChoiceField(choices=['accept', 'reject'])
    
class ConnectionListSerializer(serializers.ModelSerializer):
    """Serializer for listing connections"""
    sender = UserSearchSerializer(read_only=True)
    receiver = UserSearchSerializer(read_only=True)
    
    class Meta:
        model = Connection
        fields = ['id', 'sender', 'receiver', 'status', 'message', 'created_at', 'updated_at']
