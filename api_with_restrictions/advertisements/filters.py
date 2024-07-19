from django_filters import rest_framework as filters

from .models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    created_at = filters.DateFromToRangeFilter(field_name='created_at')
    updated_at = filters.DateFromToRangeFilter(field_name='updated_at')
    status = filters.ChoiceFilter(field_name='status')
    creator = filters.NumberFilter(field_name='creator__id')

    class Meta:
        model = Advertisement
        fields = ['title', 'description', 'created_at', 'updated_at', 'status', 'creator']
