from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import QuoteRequest, UserPreferences
from .serializers import QuoteRequestSerializer, UserPreferencesSerializer

class CreateQuoteRequestView(generics.CreateAPIView):
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure the request is made by a business user
        if self.request.user.user_type != 'business':
            raise PermissionDenied("Only businesses can request quotes.")

        expert = serializer.validated_data['expert']
        business = self.request.user
        
        # Check if the business is not requesting a quote from themselves
        if expert == business:
            raise PermissionDenied("You cannot request a quote from yourself.")
        
        # Save the quote request
        serializer.save(business=business)

class UserPreferencesView(generics.RetrieveUpdateAPIView):
    queryset = UserPreferences.objects.all()
    serializer_class = UserPreferencesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Get or create preferences for the logged-in user
        preferences, created = UserPreferences.objects.get_or_create(user=self.request.user)
        return preferences

    def perform_update(self, serializer):
        # Ensure the preferences are updated for the logged-in user
        preferences = serializer.save(user=self.request.user)
        return preferences