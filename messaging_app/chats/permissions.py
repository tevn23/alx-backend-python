"""
Custom permissions for chats app.
Ensures users can only access their own conversations/messages.
"""
from rest_framework import permissions


class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access.
    - Only participants can view/edit a conversation or its messages.
    """

    def has_permission(self, request, view):
        # Ensure user is logged in
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For Conversation
        if hasattr(obj, 'participants'):
            if request.method in ["PUT", "PATCH", "DELETE", "GET"]:
                return request.user in obj.participants.all()

        # For Message
        if hasattr(obj, 'conversation'):
            if request.method in ["PUT", "PATCH", "DELETE", "GET"]:
                return request.user in obj.conversation.participants.all()

        return False
