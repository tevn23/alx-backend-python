import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    """
    Filters for Message model:
    - sender: filter by user ID
    - start_date & end_date: filter messages in a time range
    """
    start_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ["sender", "conversation", "start_date", "end_date"]
