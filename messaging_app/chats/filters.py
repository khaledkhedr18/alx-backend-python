import django_filters
from django.db.models import Q
from .models import Message, Conversation, User

class MessageFilter(django_filters.FilterSet):
    """
    Filter class for messages to retrieve conversations with specific users
    or messages within a time range
    """
    # Filter by sender
    sender = django_filters.UUIDFilter(field_name='sender_id__user_id', lookup_expr='exact')
    sender_username = django_filters.CharFilter(field_name='sender_id__username', lookup_expr='icontains')

    # Filter by recipient
    recipient = django_filters.UUIDFilter(field_name='recipient_id__user_id', lookup_expr='exact')
    recipient_username = django_filters.CharFilter(field_name='recipient_id__username', lookup_expr='icontains')

    # Filter by conversation
    conversation = django_filters.UUIDFilter(field_name='conversation__conversation_id', lookup_expr='exact')

    # Time range filtering
    sent_after = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    sent_date = django_filters.DateFilter(field_name='sent_at', lookup_expr='date')

    # Message content filtering
    message_contains = django_filters.CharFilter(field_name='message_body', lookup_expr='icontains')

    # Custom method to filter messages with specific users
    with_user = django_filters.UUIDFilter(method='filter_with_user')

    def filter_with_user(self, queryset, name, value):
        """
        Filter messages where the current user has conversations with a specific user
        """
        if value:
            return queryset.filter(
                Q(sender_id__user_id=value) | Q(recipient_id__user_id=value)
            )
        return queryset

    class Meta:
        model = Message
        fields = [
            'sender', 'sender_username', 'recipient', 'recipient_username',
            'conversation', 'sent_after', 'sent_before', 'sent_date',
            'message_contains', 'with_user'
        ]

class ConversationFilter(django_filters.FilterSet):
    """
    Filter class for conversations
    """
    # Filter by participant
    participant = django_filters.UUIDFilter(method='filter_by_participant')
    participant_username = django_filters.CharFilter(method='filter_by_participant_username')

    # Time range filtering
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    created_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date')

    def filter_by_participant(self, queryset, name, value):
        """Filter conversations by participant user ID"""
        if value:
            return queryset.filter(participants__user_id=value)
        return queryset

    def filter_by_participant_username(self, queryset, name, value):
        """Filter conversations by participant username"""
        if value:
            return queryset.filter(participants__username__icontains=value)
        return queryset

    class Meta:
        model = Conversation
        fields = [
            'participant', 'participant_username',
            'created_after', 'created_before', 'created_date'
        ]
