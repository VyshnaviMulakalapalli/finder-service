from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from .models import CustomUser, Profile, Review
from .serializers import RegisterSerializer, ProfileSerializer, ProfileUpdateSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile

class UpdateProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "profile": serializer.data})
        return Response(serializer.errors, status=400)
    
class SubmitReviewView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        expert = serializer.validated_data['expert']
        if self.request.user == expert:
            return Response({"error": "You cannot review yourself."}, status=400)
        
        serializer.save(reviewer=self.request.user)

class UpdateDeleteReviewView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        review = super().get_object()

        # Only allow the reviewer to edit/delete their own review
        if review.reviewer != self.request.user:
            raise PermissionDenied("You can only modify your own reviews.")
        
        return review
    
class ExpertReviewPagination(PageNumberPagination):
    page_size = 5 
    page_size_query_param = "page_size"
    max_page_size = 20

class ExpertReviewsView(ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = ExpertReviewPagination

    def get_queryset(self):
        expert_id = self.kwargs["expert_id"]
        return Review.objects.filter(expert__id=expert_id).order_by("-created_at")