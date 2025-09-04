from django.urls import path
from .views import QuoteListView, QuoteDetailView

urlpatterns = [
    path('api/', QuoteListView.as_view(), name='quote-list'),
    path('<int:pk>/api/', QuoteDetailView.as_view(), name='quote-detail'),
]
# This file defines the URL patterns for the quotes app, mapping URLs to views.