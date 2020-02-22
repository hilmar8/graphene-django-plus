from django.db.models import Q

from django_filters import rest_framework as django_filters

from tests.test_app.test_app.app.models import Book


class BookFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="my_search_filter")

    class Meta:
        model = Book
        fields = ("search",)

    @classmethod
    def my_search_filter(cls, queryset, name, value):  # pylint: disable=W0613
        return queryset.filter(Q(title__istartswith=value))
