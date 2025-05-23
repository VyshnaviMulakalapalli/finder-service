from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class QuoteRequest(models.Model):
    business = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quote_requests', limit_choices_to={'user_type': 'business'})
    expert = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_quote_requests', limit_choices_to={'user_type': 'expert'})
    message = models.TextField(blank=True, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return f"Quote request from {self.business.username} to {self.expert.username} - {self.status}"
    
class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")
    saved_location = models.CharField(max_length=255, blank=True, null=True)
    saved_expertise = models.CharField(max_length=255, blank=True, null=True)
    min_rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    last_searched_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Preferences for {self.user.username}"