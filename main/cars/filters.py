from django_filters import rest_framework as filters
from cars.models import Car, Model


class CarFilter(filters.FilterSet):
    brand_name = filters.CharFilter(
        field_name="brand__name",
        lookup_expr="iexact",
        help_text="the name of the brand",
    )
    model_name = filters.CharFilter(
        field_name="model__name",
        lookup_expr="iexact",
        help_text="the name of the model",
    )
    price_min = filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
        help_text="Filter by price",
    )
    price_max = filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
        help_text="Filter by price",
    )
    year_min = filters.NumberFilter(
        field_name="year",
        lookup_expr="gte",
        help_text="Filter by minimum year of issue",
    )
    year_max = filters.NumberFilter(
        field_name="year",
        lookup_expr="lte",
        help_text="Filter by maximum year of issue",
    )
    transmission = filters.CharFilter(field_name="transmission", lookup_expr="iexact")
    engine = filters.CharFilter(field_name="engine", lookup_expr="iexact")
    exterior_color = filters.CharFilter(
        field_name="exterior_color", lookup_expr="iexact"
    )
    interior_color = filters.CharFilter(
        field_name="interior_color", lookup_expr="iexact"
    )
    mileage_min = filters.NumberFilter(
        field_name="mileage",
        lookup_expr="gte",
        help_text="Filter by minimum mileage",
    )
    mileage_max = filters.NumberFilter(
        field_name="mileage",
        lookup_expr="lte",
        help_text="Filter by maximum mileage",
    )

    fuel_type = filters.CharFilter(field_name="fuel_type", lookup_expr="iexact")

    class Meta:
        model = Car
        fields = []
