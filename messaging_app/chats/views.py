from django.shortcuts import render
from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Conversation, Message
from .serializers import (
    UserSerializer,
    UserSummarySerializer,
    ConversationSerializer,
    ConversationListSerializer,
    MessageSerializer
)

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'user_id'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'email']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['created_at', 'username']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return UserSummarySerializer
        return UserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations
    Provides CRUD operations for conversations
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'conversation_id'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['created_at']
    search_fields = ['participants__username', 'participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter conversations to only show those the user participates in"""
        user = self.request.user
        return Conversation.objects.filter(participants=user).prefetch_related(
            'participants', 'messages__sender_id', 'messages__recipient_id'
        ).distinct()

    def get_serializer_class(self):
        """Return appropriate serializer class based on action"""
        if self.action == 'list':
            return ConversationListSerializer
        return ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Add current user to participants if not included
        participants_ids = serializer.validated_data.get('participants_ids', [])
        if request.user.user_id not in participants_ids:
            participants_ids.append(request.user.user_id)
            serializer.validated_data['participants_ids'] = participants_ids

        conversation = serializer.save()

        # Return detailed conversation data
        response_serializer = ConversationSerializer(conversation, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, conversation_id=None):
        """Add a participant to existing conversation"""
        conversation = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(user_id=user_id)
            conversation.participants.add(user)

            serializer = self.get_serializer(conversation)
            return Response(serializer.data)

        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def remove_participant(self, request, conversation_id=None):
        """Remove a participant from existing conversation"""
        conversation = self.get_object()
        user_id = request.data.get('user_id')

        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(user_id=user_id)
            conversation.participants.remove(user)

            serializer = self.get_serializer(conversation)
            return Response(serializer.data)

        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'])
    def messages(self, request, conversation_id=None):
        """Get all messages in a conversation"""
        conversation = self.get_object()
        messages = conversation.messages.all().order_by('-sent_at')

        # Pagination
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = MessageSerializer(messages, many=True, context={'request': request})
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages
    Provides CRUD operations for messages
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'message_id'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sender_id', 'recipient_id', 'conversation', 'sent_at']
    search_fields = ['message_body', 'sender_id__username', 'recipient_id__username']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        """Filter messages to only show those the user can access"""
        user = self.request.user
        queryset = Message.objects.filter(
            Q(sender_id=user) | Q(recipient_id=user)
        ).select_related('sender_id', 'recipient_id', 'conversation').order_by('-sent_at')

        # Handle nested routing - filter by conversation if provided
        conversation_pk = self.kwargs.get('conversation_pk')
        if conversation_pk:
            queryset = queryset.filter(conversation__conversation_id=conversation_pk)

        # Custom filtering based on query parameters
        sender_id = self.request.query_params.get('sender_id')
        recipient_id = self.request.query_params.get('recipient_id')
        conversation_id = self.request.query_params.get('conversation')

        if sender_id:
            queryset = queryset.filter(sender_id__user_id=sender_id)
        if recipient_id:
            queryset = queryset.filter(recipient_id__user_id=recipient_id)
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)

        return queryset

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation
        """
        # Set sender_id to current user
        request.data['sender_id'] = str(request.user.user_id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verify user has access to the conversation
        conversation_id = serializer.validated_data.get('conversation')
        if conversation_id:
            conversation = get_object_or_404(
                Conversation,
                conversation_id=conversation_id.conversation_id,
                participants=request.user
            )

        message = serializer.save()
        return Response(
            MessageSerializer(message, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        """Update message - only sender can update their own messages"""
        message = self.get_object()

        if message.sender_id != request.user:
            return Response(
                {'error': 'You can only edit your own messages'},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete message - only sender can delete their own messages"""
        message = self.get_object()

        if message.sender_id != request.user:
            return Response(
                {'error': 'You can only delete your own messages'},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def sent(self, request):
        """Get messages sent by current user"""
        messages = self.get_queryset().filter(sender_id=request.user)

        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def received(self, request):
        """Get messages received by current user"""
        messages = self.get_queryset().filter(recipient_id=request.user)

        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def send_to_conversation(self, request):
        """
        Send a message to a specific conversation
        Expects: conversation_id, recipient_id, message_body
        """
        conversation_id = request.data.get('conversation_id')
        recipient_id = request.data.get('recipient_id')
        message_body = request.data.get('message_body')

        if not all([conversation_id, recipient_id, message_body]):
            return Response(
                {'error': 'conversation_id, recipient_id, and message_body are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify conversation exists and user participates in it
        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_id,
                participants=request.user
            )
        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found or access denied'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Verify recipient is in the conversation
        try:
            recipient = User.objects.get(user_id=recipient_id)
            if recipient not in conversation.participants.all():
                return Response(
                    {'error': 'Recipient is not part of this conversation'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                {'error': 'Recipient not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Create message
        message_data = {
            'sender_id': str(request.user.user_id),
            'recipient_id': recipient_id,
            'conversation': conversation_id,
            'message_body': message_body
        }

        serializer = self.get_serializer(data=message_data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        return Response(
            MessageSerializer(message, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )
