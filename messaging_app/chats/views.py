from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwnerOrParticipant


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Conversations.
    - list all conversations (only user’s own)
    - create a new conversation
    - custom action: list messages in a conversation
    """
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email', 'participants__first_name', 'participants__last_name']
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrParticipant]

    def get_queryset(self):
        """Limit conversations to only those the user participates in."""
        user = self.request.user
        return Conversation.objects.filter(participants=user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expects: { "participants": [user_id1, user_id2, ...] }
        """
        participants = request.data.get("participants", [])
        if not participants:
            return Response({"error": "Participants required"}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants + [request.user.id])  # ensure creator is included
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        """
        Custom endpoint: /conversations/{id}/messages/
        Lists messages in this conversation.
        """
        conversation = self.get_object()  # permission check runs here
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Messages.
    - list messages (only those in user’s conversations)
    - create a message in a conversation
    """
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['sender__email', 'conversation__conversation_id', 'message_body']
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrParticipant]

    def get_queryset(self):
        """Limit messages to only those in conversations the user is part of."""
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)

    def create(self, request, *args, **kwargs):
        """
        Send a new message.
        Expects: { "conversation": <conversation_id>, "sender": <user_id>, "message_body": "text" }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
