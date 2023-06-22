from comments.views import CommentsModelViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"", CommentsModelViewSet)

urlpatterns = []

urlpatterns.extend(router.urls)
