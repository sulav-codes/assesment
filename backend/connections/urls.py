from django.urls import path
from .views import (
    ConnectionRequestView,
    ConnectionListView,
    respond_to_connection,
    cancel_connection_request,
    connection_status
)

app_name = 'connections'

urlpatterns = [
    path('request/', ConnectionRequestView.as_view(), name='request'),
    path('list/', ConnectionListView.as_view(), name='list'),
    path('respond/<int:connection_id>/', respond_to_connection, name='respond'),
    path('cancel/<int:connection_id>/', cancel_connection_request, name='cancel'),
    path('status/<int:user_id>/', connection_status, name='status'),
]