from django.contrib import admin
from django.urls import path
from .views import educator_dash

urlpatterns = [
    path('educator_dashboard/', educator_dash),
]
