from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Activity, Team, Leaderboard, WorkoutSuggestion


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'username', 'email', 'bio', 'avatar_url', 'age',
            'height', 'weight', 'activity_level', 'fitness_goals',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Activity
        fields = [
            'id', 'user', 'username', 'activity_type', 'title', 'description',
            'duration_minutes', 'calories_burned', 'distance_km', 'intensity_level',
            'activity_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    leader_name = serializers.CharField(source='leader.username', read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'leader', 'leader_name',
            'member_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_member_count(self, obj):
        return obj.members.count()


class TeamDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Team with members"""
    leader_name = serializers.CharField(source='leader.username', read_only=True)
    members = UserSerializer(many=True, read_only=True)
    total_calories = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'leader', 'leader_name',
            'members', 'total_calories', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_total_calories(self, obj):
        return obj.get_total_calories()


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    username = serializers.CharField(source='user.username', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Leaderboard
        fields = [
            'id', 'team', 'team_name', 'user', 'username',
            'challenge_week', 'challenge_year', 'total_calories',
            'total_activities', 'rank', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WorkoutSuggestionSerializer(serializers.ModelSerializer):
    """Serializer for WorkoutSuggestion model"""
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = WorkoutSuggestion
        fields = [
            'id', 'user', 'username', 'title', 'description',
            'suggested_activity', 'suggested_duration_minutes', 'difficulty_level',
            'reason', 'created_at', 'completed', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at']
