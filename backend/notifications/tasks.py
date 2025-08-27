from celery import shared_task
from django.utils import timezone
from .models import Notification
from connections.models import Connection

@shared_task
def send_connection_notification(connection_id, notification_type):
    """Send notification for connection events"""
    try:
        connection = Connection.objects.get(id=connection_id)
        
        if notification_type == 'connection_request':
            # Notify receiver about new connection request
            Notification.objects.create(
                user=connection.receiver,
                sender=connection.sender,
                notification_type='connection_request',
                title='New Connection Request',
                message=f'{connection.sender.full_name} wants to connect with you.',
                connection=connection
            )
        
        elif notification_type == 'connection_accepted':
            # Notify sender that request was accepted
            Notification.objects.create(
                user=connection.sender,
                sender=connection.receiver,
                notification_type='connection_accepted',
                title='Connection Request Accepted',
                message=f'{connection.receiver.full_name} accepted your connection request.',
                connection=connection
            )
        
        elif notification_type == 'connection_rejected':
            # Notify sender that request was rejected
            Notification.objects.create(
                user=connection.sender,
                sender=connection.receiver,
                notification_type='connection_rejected',
                title='Connection Request Rejected',
                message=f'{connection.receiver.full_name} rejected your connection request.',
                connection=connection
            )
        
        return f"Notification sent for {notification_type}"
    
    except Connection.DoesNotExist:
        return f"Connection {connection_id} not found"
    except Exception as e:
        return f"Error sending notification: {str(e)}"

@shared_task
def cleanup_old_notifications():
    """Clean up old notifications (older than 30 days)"""
    from datetime import timedelta
    
    cutoff_date = timezone.now() - timedelta(days=30)
    deleted_count = Notification.objects.filter(
        created_at__lt=cutoff_date,
        is_deleted=True
    ).delete()[0]
    
    return f"Cleaned up {deleted_count} old notifications"