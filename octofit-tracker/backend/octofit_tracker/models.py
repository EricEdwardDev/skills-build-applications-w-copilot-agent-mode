from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum, Q
from datetime import timedelta


class UserProfile(models.Model):
    """Extended user profile for fitness tracking"""
    ACTIVITY_LEVELS = [
        ('sedentary', 'Sedentary'),
        ('lightly_active', 'Lightly Active'),
        ('moderately_active', 'Moderately Active'),
        ('very_active', 'Very Active'),
        ('extremely_active', 'Extremely Active'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    height = models.FloatField(help_text="Height in cm", blank=True, null=True)
    weight = models.FloatField(help_text="Weight in kg", blank=True, null=True)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVELS, default='moderately_active')
    fitness_goals = models.TextField(blank=True, null=True, help_text="Comma-separated fitness goals")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

    class Meta:
        db_table = 'user_profiles'


class Activity(models.Model):
    """User fitness activity tracking"""
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('walking', 'Walking'),
        ('gym', 'Gym Workout'),
        ('yoga', 'Yoga'),
        ('sports', 'Sports'),
        ('hiking', 'Hiking'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    duration_minutes = models.IntegerField(help_text="Duration in minutes")
    calories_burned = models.IntegerField(help_text="Estimated calories burned")
    distance_km = models.FloatField(blank=True, null=True, help_text="Distance in kilometers")
    intensity_level = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    activity_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.activity_date}"

    class Meta:
        db_table = 'activities'
        ordering = ['-activity_date']


class Team(models.Model):
    """Team management for group fitness challenges"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='led_teams')
    members = models.ManyToManyField(User, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - Led by {self.leader.username if self.leader else 'N/A'}"

    def get_total_calories(self, days=7):
        """Calculate total calories burned by team members in last N days"""
        start_date = timezone.now() - timedelta(days=days)
        return Activity.objects.filter(
            user__teams=self,
            activity_date__gte=start_date
        ).aggregate(total=Sum('calories_burned'))['total'] or 0

    class Meta:
        db_table = 'teams'


class Leaderboard(models.Model):
    """Leaderboard tracking for competitive fitness"""
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='leaderboards')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    challenge_week = models.IntegerField()
    challenge_year = models.IntegerField()
    total_calories = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    rank = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Rank {self.rank} in {self.team.name}"

    class Meta:
        db_table = 'leaderboards'
        unique_together = ['team', 'user', 'challenge_week', 'challenge_year']
        ordering = ['team', 'rank']


class WorkoutSuggestion(models.Model):
    """Personalized workout suggestions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_suggestions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    suggested_activity = models.CharField(max_length=20, choices=Activity.ACTIVITY_TYPES)
    suggested_duration_minutes = models.IntegerField()
    difficulty_level = models.CharField(
        max_length=20,
        choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]
    )
    reason = models.TextField(help_text="Why this suggestion was made")
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Suggestion for {self.user.username}: {self.title}"

    class Meta:
        db_table = 'workout_suggestions'
        ordering = ['-created_at']
