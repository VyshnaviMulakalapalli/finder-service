from django.urls import path
from .views import CreateQuoteRequestView, UserPreferencesView

urlpatterns = [
    path('quote-requests/', CreateQuoteRequestView.as_view(), name='create-quote-request'),
    path('preferences/', UserPreferencesView.as_view(), name='user-preferences'),
]