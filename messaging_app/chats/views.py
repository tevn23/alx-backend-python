from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Conversations.
    - list all conversations
    - create a new conversation
    - custom action: list messages in a conversation
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilters]
    search_fields = ['participants__email', 'participants__first_name', 'participants__last_name']

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expects: { "participants": [user_id1, user_id2, ...] }
        """
        participants = request.data.get("participants", [])
        if not participants:
            return Response({"error": "Participants required"}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)  # ManyToMany assignment
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        """
        Custom endpoint: /conversations/{id}/messages/
        Lists messages in this conversation.
        """
        conversation = self.get_object()
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Messages.
    - list all messages
    - create a message in a conversation
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilters]
    search_fields = ['sender__email', 'conversation__conversation_id', 'message_body']

    def create(self, request, *args, **kwargs):
        """
        Send a new message.
        Expects: { "conversation": <conversation_id>, "sender": <user_id>, "message_body": "text" }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
