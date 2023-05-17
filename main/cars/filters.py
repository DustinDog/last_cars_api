from django_filters import rest_framework as filters
from cars.models import Car, Model


class ModelFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", help_text="the name of the model")

    body_style = filters.CharFilter(
        field_name="body_style",
        help_text="the body style of the model (hatcback, sedan, etc.)",
    )

    class Meta:
        model = Model
        fields = ["name", "body_style", "brand__name"]


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

    class Meta:
        model = Car
        fields = ["brand_name", "model_name"]
