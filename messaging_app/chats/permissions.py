"""
Custom permissions for chats app.
Ensures users can only access their own conversations/messages.
"""
from rest_framework import permissions

class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission: Only participants can view/edit a conversation or its messages.
    """

    def has_object_permission(self, request, view, obj):
        # Always allow superusers
        if request.user and request.user.is_superuser:
            return True
            
        # For Conversation
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # For Message
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False
