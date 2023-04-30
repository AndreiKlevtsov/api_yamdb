import django_filters
from django_filters import FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')
    year = django_filters.CharFilter(field_name='year')
    name = django_filters.CharFilter(field_name='name')

    class Meta:
        model = Title
        fields = ['genre__slug', 'category__slug', 'year', 'name']
