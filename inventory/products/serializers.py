from django.db.models import fields
from products.utils import is_constraint_valid
from products.models import Box
from rest_framework.serializers import ModelSerializer, ValidationError


class BoxSerializer(ModelSerializer):
    class Meta:
        model = Box
        fields = ("id", "length", "width", "height", "area", "volume")


class BoxCreateSerializer(ModelSerializer):
    class Meta:
        model = Box
        fields = (
            "id",
            "length",
            "width",
            "height",
            "area",
            "volume",
            "created_by",
            "last_updated",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "last_updated": {"read_only": True},
        }


class StaffBoxSerializer(ModelSerializer):
    class Meta:
        model = Box
        fields = (
            "id",
            "length",
            "width",
            "height",
            "area",
            "volume",
            "created_by",
            "last_updated",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "created_by": {"read_only": True},
            "last_updated": {"read_only": True},
        }

    def validate(self, data):
        print(data["length"])
        request = self.context.get("request")
        user = request.user
        if is_constraint_valid(user, data):
            return data
