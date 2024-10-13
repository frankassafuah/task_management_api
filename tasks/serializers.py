from django.utils import timezone
from rest_framework import serializers
from .models import Task


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ["id", "username", "email", "password"]
#         extra_kwargs = {"password": {"write_only": True}}

#     def create(self, validated_data):
#         user = CustomUser(
#             email=validated_data["email"], username=validated_data["username"]
#         )
#         user.set_password(validated_data["password"])
#         user.save()
#         return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "due_date",
            "priority",
            "status",
            "completed_at",
        ]

    def validate_due_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("The due date must be in the future.")
        return value
