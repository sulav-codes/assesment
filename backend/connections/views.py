from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Connection
from .serializers import (
    ConnectionRequestSerializer,
    ConnectionResponseSerializer,
    ConnectionListSerializer
)
from notifications.tasks import send_connection_notification

class ConnectionRequestView(generics.CreateAPIView):
    """API endpoint for sending connection requests"""
    serializer_class = ConnectionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        connection = serializer.save(sender=self.request.user)
        
        # Send async notification
        send_connection_notification.delay(
            connection.id,
            'connection_request'
        )
    
    def create(self, request, *args, **kwargs):
        """Override to return full connection object"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        connection = serializer.save(sender=request.user)
        
        # Send async notification
        send_connection_notification.delay(
            connection.id,
            'connection_request'
        )
        
        # Return full connection data using ConnectionListSerializer
        response_serializer = ConnectionListSerializer(connection)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class ConnectionListView(generics.ListAPIView):
    """API endpoint for listing user connections"""
    serializer_class = ConnectionListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        status_filter = self.request.query_params.get('status', None)
        connection_type = self.request.query_params.get('type', 'all')
        
        # Base queryset
        if connection_type == 'sent':
            queryset = Connection.objects.filter(sender=user)
        elif connection_type == 'received':
            queryset = Connection.objects.filter(receiver=user)
        else:
            queryset = Connection.objects.filter(
                Q(sender=user) | Q(receiver=user)
            )
        
        # Filter by status if provided
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def respond_to_connection(request, connection_id):
    """API endpoint for responding to connection requests"""
    connection = get_object_or_404(
        Connection, 
        id=connection_id, 
        receiver=request.user,
        status='pending'
    )
    
    serializer = ConnectionResponseSerializer(data=request.data)
    if serializer.is_valid():
        action = serializer.validated_data['action']
        
        if action == 'accept':
            connection.status = 'accepted'
            message = 'Connection request accepted'
        else:
            connection.status = 'rejected'
            message = 'Connection request rejected'
        
        connection.save()
        
        # Send async notification
        send_connection_notification.delay(
            connection.id,
            f'connection_{action}ed'
        )
        
        return Response({
            'message': message,
            'connection': ConnectionListSerializer(connection).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def cancel_connection_request(request, connection_id):
    """API endpoint for canceling sent connection requests"""
    connection = get_object_or_404(
        Connection,
        id=connection_id,
        sender=request.user,
        status='pending'
    )
    
    connection.delete()
    
    return Response({
        'message': 'Connection request canceled'
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def connection_status(request, user_id):
    """API endpoint to check connection status with another user"""
    user = request.user
    
    connection = Connection.objects.filter(
        Q(sender=user, receiver_id=user_id) |
        Q(sender_id=user_id, receiver=user)
    ).first()
    
    if connection:
        return Response({
            'status': connection.status,
            'is_sender': connection.sender == user,
            'connection_id': connection.id
        })
    
    return Response({
        'status': 'none',
        'is_sender': False,
        'connection_id': None
    })
