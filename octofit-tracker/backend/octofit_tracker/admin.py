from django.contrib import admin
from .models import UserProfile, Activity, Team, Leaderboard, WorkoutSuggestion


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'weight', 'activity_level', 'created_at']
    list_filter = ['activity_level', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'title', 'duration_minutes', 'calories_burned', 'activity_date']
    list_filter = ['activity_type', 'intensity_level', 'activity_date']
    search_fields = ['user__username', 'title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'activity_date'


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader', 'get_member_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description', 'leader__username']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['members']

    def get_member_count(self, obj):
        return obj.members.count()
    get_member_count.short_description = 'Members'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'team', 'rank', 'total_calories', 'total_activities']
    list_filter = ['team', 'challenge_week', 'challenge_year']
    search_fields = ['user__username', 'team__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['team', 'rank']


@admin.register(WorkoutSuggestion)
class WorkoutSuggestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'suggested_activity', 'difficulty_level', 'completed', 'created_at']
    list_filter = ['suggested_activity', 'difficulty_level', 'completed', 'created_at']
    search_fields = ['user__username', 'title', 'description']
    readonly_fields = ['created_at']
