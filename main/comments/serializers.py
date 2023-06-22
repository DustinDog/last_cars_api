from comments.models import Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "car",
            "user",
            "created",
            "text",
            "parent",
        )


class RetrieveCommentSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "car",
            "user",
            "created",
            "text",
            "parent",
            "reply_count",
            "replies",
        )

    def get_reply_count(self, obj):
        return obj.my_children().count()

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentSerializer(obj.my_children(), many=True).data

        return None


class WriteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "car",
            "created",
            "text",
            "parent",
        )

    def validate(self, data):
        parent = data.get("parent")
        if parent and parent.parent:
            data["parent"] = parent.parent

        return super().validate(data)

    def create(self, validated_data):
        user = self.context["request"].user
        comment = Comment.objects.create(**validated_data, user=user)
        return comment
