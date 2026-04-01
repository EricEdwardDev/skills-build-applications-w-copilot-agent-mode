from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta

from .models import UserProfile, Activity, Team, Leaderboard, WorkoutSuggestion
from .serializers import (
    UserSerializer, UserProfileSerializer, ActivitySerializer,
    TeamSerializer, TeamDetailSerializer, LeaderboardSerializer,
    WorkoutSuggestionSerializer
)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile model"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current user's profile"""
        try:
            profile = request.user.profile
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activity model"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['activity_date', 'calories_burned']
    ordering = ['-activity_date']

    def get_queryset(self):
        """Return activities for current user or all if staff"""
        if self.request.user.is_staff:
            return Activity.objects.all()
        return Activity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create activity for current user"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_activities(self, request):
        """Get current user's activities"""
        activities = Activity.objects.filter(user=request.user)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def this_week(self, request):
        """Get activities from this week"""
        start_date = timezone.now() - timedelta(days=7)
        activities = Activity.objects.filter(
            user=request.user,
            activity_date__gte=start_date
        )
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get activity statistics"""
        activities = Activity.objects.filter(user=request.user)
        stats = {
            'total_activities': activities.count(),
            'total_calories': activities.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0,
            'total_distance': activities.aggregate(Sum('distance_km'))['distance_km__sum'] or 0,
            'total_duration': activities.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0,
        }
        return Response(stats)


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for Team model"""
    queryset = Team.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeamDetailSerializer
        return TeamSerializer

    @action(detail=False, methods=['post'])
    def create_team(self, request):
        """Create a new team"""
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            team = serializer.save(leader=request.user)
            team.members.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add a member to the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            team.members.add(user)
            return Response({'status': 'Member added'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        """Remove a member from the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
            team.members.remove(user)
            return Response({'status': 'Member removed'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def leaderboard(self, request, pk=None):
        """Get team leaderboard"""
        team = self.get_object()
        leaderboard = team.leaderboards.all()
        serializer = LeaderboardSerializer(leaderboard, many=True)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """ViewSet for Leaderboard model"""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['rank', 'total_calories']
    ordering = ['rank']

    @action(detail=False, methods=['get'])
    def current_week(self, request):
        """Get leaderboard for current week"""
        from datetime import datetime
        now = datetime.now()
        leaderboards = Leaderboard.objects.filter(
            challenge_week=now.isocalendar()[1],
            challenge_year=now.isocalendar()[0]
        )
        serializer = self.get_serializer(leaderboards, many=True)
        return Response(serializer.data)


class WorkoutSuggestionViewSet(viewsets.ModelViewSet):
    """ViewSet for WorkoutSuggestion model"""
    queryset = WorkoutSuggestion.objects.all()
    serializer_class = WorkoutSuggestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return suggestions for current user"""
        if self.request.user.is_staff:
            return WorkoutSuggestion.objects.all()
        return WorkoutSuggestion.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get pending suggestions"""
        suggestions = WorkoutSuggestion.objects.filter(
            user=request.user,
            completed=False
        )
        serializer = self.get_serializer(suggestions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Mark suggestion as completed"""
        suggestion = self.get_object()
        suggestion.completed = True
        suggestion.completed_at = timezone.now()
        suggestion.save()
        serializer = self.get_serializer(suggestion)
        return Response(serializer.data)
