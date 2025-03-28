from rest_framework import serializers
from .models import QuoteRequest

class QuoteRequestSerializer(serializers.ModelSerializer):
    business = serializers.CharField(source="business.username", read_only=True)
    expert = serializers.CharField(source="expert.username", read_only=True)

    class Meta:
        model = QuoteRequest
        fields = ['business', 'expert', 'message', 'status', 'requested_at']
        read_only_fields = ['business', 'expert', 'requested_at']