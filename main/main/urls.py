from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin

api_urls = [
    path("", include("core.urls")),
    path("cars/", include("cars.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urls)),
    path("__debug__/", include("debug_toolbar.urls")),
]
