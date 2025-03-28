from django.urls import path
from .views import CreateQuoteRequestView

urlpatterns = [
    path('quote-requests/', CreateQuoteRequestView.as_view(), name='create-quote-request'),
]