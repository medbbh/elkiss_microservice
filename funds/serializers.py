from rest_framework import serializers
from .models import Fund
from django.utils import timezone

class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = '__all__'
        read_only_fields = [
            "owner",
            "current_amount",
            "total_participants",
            "created_at",
            "updated_at",
        ]

    # Validate that deadline is in the future.
    def validate_deadline(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("Deadline must be in the future.")
        return value

