import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):

    class Meta:
        model=Product
        fields=[
            "category",
            "status",
            "owner",
        ]






# NOTES
# django-filter

# A package that makes query-parameter based filtering easier.

# FilterSet
# class ProductFilter(django_filters.FilterSet):

# Defines which model fields can be filtered.

# fields
# fields = [
#     "category",
#     "status",
#     "owner",
# ]

# Defines filterable fields.

# filterset.qs
# products = filterset.qs

# Returns the queryset after applying the requested filters.