from cars.models import Car
from django.contrib.auth import get_user_model
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class Comment(MPTTModel):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, null=False, blank=False, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=1000)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["id"]

    @property
    def is_parent(self):
        return self.parent is None

    def my_children(self):
        return self.get_descendants()

    def __str__(self):
        return f"{self.id}"
