from rest_framework import serializers
from .models import CustomUser, Profile, Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'user_type', 'phone']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'user_type', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['location', 'expertise', 'bio']

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.ReadOnlyField(source="reviewer.username")

    class Meta:
        model = Review
        fields = ["id", "expert", "reviewer", "rating", "comment", "created_at"]
        read_only_fields = ["id", "reviewer", "created_at"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value