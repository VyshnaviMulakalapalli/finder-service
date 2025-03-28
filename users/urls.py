from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import RegisterView, ProfileView, UpdateProfileView, SubmitReviewView, UpdateDeleteReviewView, ExpertReviewsView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path('submit-review/', SubmitReviewView.as_view(), name='submit-review'),
    path('review/<int:pk>/', UpdateDeleteReviewView.as_view(), name='update-delete-review'),
    path('expert/<int:expert_id>/reviews/', ExpertReviewsView.as_view(), name='expert-reviews'),
]