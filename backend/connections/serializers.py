from rest_framework import serializers
from django.db import models
from django.contrib.auth import get_user_model
from .models import Connection
from users.serializers import UserSearchSerializer

User = get_user_model()

class ConnectionRequestSerializer(serializers.ModelSerializer):
    """Serializer for creating connection requests"""
    receiver = serializers.CharField(max_length=150, write_only=True)
    
    class Meta:
        model = Connection
        fields = ['receiver', 'message']
    
    def validate_receiver(self, value):
        """Ensure user exists and user cannot send request to themselves"""
        request = self.context.get('request')
        
        # Check if user exists by username
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this username does not exist.")
        
        # Ensure user cannot send request to themselves
        if request and request.user.username == value:
            raise serializers.ValidationError("You cannot send a connection request to yourself.")
        
        return value
    
    def validate(self, attrs):
        """Check if connection already exists"""
        request = self.context.get('request')
        receiver_username = attrs.get('receiver')
        
        if request:
            # Get the receiver user object by username
            receiver = User.objects.get(username=receiver_username)
            
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
        receiver_username = validated_data.pop('receiver')
        receiver = User.objects.get(username=receiver_username)
        
        validated_data['sender'] = request.user
        validated_data['receiver'] = receiver
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
