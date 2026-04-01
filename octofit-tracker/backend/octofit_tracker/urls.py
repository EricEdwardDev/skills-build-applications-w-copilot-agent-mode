from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

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
