from rest_framework import serializers
from .models import QuoteRequest, UserPreferences

class QuoteRequestSerializer(serializers.ModelSerializer):
    business = serializers.CharField(source="business.username", read_only=True)
    expert = serializers.CharField(source="expert.username", read_only=True)

    class Meta:
        model = QuoteRequest
        fields = ['business', 'expert', 'message', 'status', 'requested_at']
        read_only_fields = ['business', 'expert', 'requested_at']

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ['saved_location', 'saved_expertise', 'min_rating', 'last_searched_at']
        read_only_fields = ['last_searched_at']