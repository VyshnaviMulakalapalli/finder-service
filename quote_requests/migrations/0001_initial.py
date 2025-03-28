# Generated by Django 5.1.7 on 2025-03-28 16:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QuoteRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True)),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('business', models.ForeignKey(limit_choices_to={'user_type': 'business'}, on_delete=django.db.models.deletion.CASCADE, related_name='quote_requests', to=settings.AUTH_USER_MODEL)),
                ('expert', models.ForeignKey(limit_choices_to={'user_type': 'expert'}, on_delete=django.db.models.deletion.CASCADE, related_name='received_quote_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
