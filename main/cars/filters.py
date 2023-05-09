from django_filters import rest_framework as filters
from cars.models import Brand, Car, Model


class ModelFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", help_text="the name of the model ")
    year_min = filters.NumberFilter(field_name="year_of_issue", lookup_expr="gte")
    year_max = filters.NumberFilter(field_name="year_of_issue", lookup_expr="lte")
    body_style = filters.CharFilter(field_name="body_style")
    brand_name = filters.CharFilter(field_name="brand_name")

    class Meta:
        model = Model
        fields = ["name", "year_min", "year_max", "body_style", "brand_name"]


class CarFilter(filters.FilterSet):
    brand_name = filters.CharFilter(
        field_name="brand__name", lookup_expr="iexact", help_text="does it work"
    )
    model_name = filters.CharFilter(field_name="model__name", lookup_expr="iexact")
    year_min = filters.NumberFilter(
        field_name="model__year_of_issue", lookup_expr="gte"
    )
    year_max = filters.NumberFilter(
        field_name="model__year_of_issue", lookup_expr="lte"
    )

    class Meta:
        model = Car
        fields = "__all__"
