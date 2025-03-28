from rest_framework import generics, permissions, filters
from rest_framework.permissions import AllowAny
from .models import CustomUser, Profile, Review
from .serializers import RegisterSerializer, ProfileSerializer, ProfileUpdateSerializer, ReviewSerializer, ExpertSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

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
    
class ExpertSearchView(generics.ListAPIView):
    queryset = Profile.objects.filter(user__user_type='expert')
    serializer_class = ExpertSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['location', 'expertise', 'user__username']

    def get_queryset(self):
        queryset = self.queryset
        location = self.request.query_params.get('location')
        expertise = self.request.query_params.get('expertise')
        min_rating = self.request.query_params.get('min_rating')

        if location and expertise and min_rating:
            queryset = queryset.filter(
                Q(location__icontains=location) &
                Q(expertise__icontains=expertise) &
                Q(rating__gte=min_rating)
            )
        if location:
            queryset = queryset.filter(location__icontains=location)
        if expertise:
            queryset = queryset.filter(expertise__icontains=expertise)
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)

        return queryset