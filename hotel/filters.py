import django_filters
from django_filters import DateFilter, CharFilter

from .models import *


class RoomFilter(django_filters.FilterSet):
    # status = CharFilter(field_name='status', lookup_expr='icontains')

    class Meta:
        model = RoomDetail
        fields = '__all__'
        exclude = ['type']
