from django_filters import rest_framework as filters
from cars.models import Car, Model


class ModelFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", help_text="the name of the model")
    year_min = filters.NumberFilter(
        field_name="year_of_issue",
        lookup_expr="gte",
        help_text="the year of issue of the model",
    )
    year_max = filters.NumberFilter(
        field_name="year_of_issue",
        lookup_expr="lte",
        help_text="the year of issue of the model",
    )
    body_style = filters.CharFilter(
        field_name="body_style",
        help_text="the body style of the model (hatcback, sedan, etc.)",
    )

    class Meta:
        model = Model
        fields = ["name", "year_min", "year_max", "body_style", "brand__name"]


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
    year_min = filters.NumberFilter(
        field_name="model__year_of_issue",
        lookup_expr="gte",
        help_text="the year of issue of the model",
    )
    year_max = filters.NumberFilter(
        field_name="model__year_of_issue",
        lookup_expr="lte",
        help_text="the year of issue of the model",
    )

    class Meta:
        model = Car
        fields = ["brand_name", "model_name", "year_min", "year_max"]
