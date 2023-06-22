from comments.models import Comment
from comments.permissions import isCommentOwner
from comments.serializers import RetrieveCommentSerializer, WriteCommentSerializer
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.viewsets import ModelViewSet


class CommentsModelViewSet(ModelViewSet):
    queryset = Comment.objects.select_related(
        "parent",
    )

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticated, isCommentOwner]

        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RetrieveCommentSerializer
        else:
            return WriteCommentSerializer
