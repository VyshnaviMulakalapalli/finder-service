from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import QuoteRequest
from .serializers import QuoteRequestSerializer

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