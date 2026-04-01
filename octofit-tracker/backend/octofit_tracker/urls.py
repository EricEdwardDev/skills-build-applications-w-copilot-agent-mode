from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from . import views

# Codespace URL configuration
codespace_name = os.environ.get('CODESPACE_NAME')
if codespace_name:
    base_url = f"https://{codespace_name}-8000.app.github.dev"
else:
    base_url = "http://localhost:8000"

router = DefaultRouter()
router.register(r'users/profiles', views.UserProfileViewSet, basename='userprofile')
router.register(r'activities', views.ActivityViewSet, basename='activity')
router.register(r'teams', views.TeamViewSet, basename='team')
router.register(r'leaderboards', views.LeaderboardViewSet, basename='leaderboard')
router.register(r'suggestions', views.WorkoutSuggestionViewSet, basename='suggestion')

app_name = 'octofit_tracker'

urlpatterns = [
    path('', include(router.urls)),
]
