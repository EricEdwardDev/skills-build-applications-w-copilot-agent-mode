from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import UserProfile, Activity, Team, Leaderboard, WorkoutSuggestion


class UserProfileTestCase(TestCase):
    """Test cases for UserProfile model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )

    def test_create_user_profile(self):
        """Test creating a user profile"""
        profile = UserProfile.objects.create(
            user=self.user,
            age=25,
            height=175,
            weight=70,
            activity_level='moderately_active'
        )
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.age, 25)
        self.assertEqual(profile.weight, 70)

    def test_user_profile_str_method(self):
        """Test UserProfile __str__ method"""
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(str(profile), f"Profile for {self.user.username}")


class ActivityTestCase(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )

    def test_create_activity(self):
        """Test creating an activity"""
        activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            title='Morning Run',
            duration_minutes=30,
            calories_burned=300,
            distance_km=5.0,
            activity_date=timezone.now()
        )
        self.assertEqual(activity.user.username, 'testuser')
        self.assertEqual(activity.activity_type, 'running')
        self.assertEqual(activity.calories_burned, 300)

    def test_activity_str_method(self):
        """Test Activity __str__ method"""
        activity = Activity.objects.create(
            user=self.user,
            activity_type='cycling',
            title='Cycling',
            duration_minutes=45,
            calories_burned=400,
            activity_date=timezone.now()
        )
        self.assertIn('testuser', str(activity))
        self.assertIn('cycling', str(activity))


class TeamTestCase(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )

    def test_create_team(self):
        """Test creating a team"""
        team = Team.objects.create(
            name='Fitness Warriors',
            description='Elite fitness team',
            leader=self.user1
        )
        team.members.add(self.user1, self.user2)
        
        self.assertEqual(team.name, 'Fitness Warriors')
        self.assertEqual(team.leader, self.user1)
        self.assertEqual(team.members.count(), 2)

    def test_team_get_total_calories(self):
        """Test team total calories calculation"""
        team = Team.objects.create(name='Test Team', leader=self.user1)
        team.members.add(self.user1, self.user2)
        
        # Create activities for team members
        Activity.objects.create(
            user=self.user1,
            activity_type='running',
            title='Run',
            duration_minutes=30,
            calories_burned=300,
            activity_date=timezone.now()
        )
        Activity.objects.create(
            user=self.user2,
            activity_type='cycling',
            title='Cycle',
            duration_minutes=45,
            calories_burned=400,
            activity_date=timezone.now()
        )
        
        total_calories = team.get_total_calories(days=7)
        self.assertEqual(total_calories, 700)


class LeaderboardTestCase(TestCase):
    """Test cases for Leaderboard model"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass123')
        self.user2 = User.objects.create_user(username='user2', password='testpass123')
        self.team = Team.objects.create(name='Test Team', leader=self.user1)

    def test_create_leaderboard_entry(self):
        """Test creating a leaderboard entry"""
        leaderboard = Leaderboard.objects.create(
            team=self.team,
            user=self.user1,
            challenge_week=1,
            challenge_year=2026,
            total_calories=1000,
            total_activities=5,
            rank=1
        )
        self.assertEqual(leaderboard.rank, 1)
        self.assertEqual(leaderboard.total_calories, 1000)

    def test_leaderboard_unique_constraint(self):
        """Test leaderboard unique constraint"""
        Leaderboard.objects.create(
            team=self.team,
            user=self.user1,
            challenge_week=1,
            challenge_year=2026,
            total_calories=1000,
            rank=1
        )
        
        # Should raise IntegrityError due to unique constraint
        with self.assertRaises(Exception):
            Leaderboard.objects.create(
                team=self.team,
                user=self.user1,
                challenge_week=1,
                challenge_year=2026,
                total_calories=1500,
                rank=1
            )


class WorkoutSuggestionTestCase(TestCase):
    """Test cases for WorkoutSuggestion model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_create_workout_suggestion(self):
        """Test creating a workout suggestion"""
        suggestion = WorkoutSuggestion.objects.create(
            user=self.user,
            title='Morning Yoga',
            description='Start your day with yoga',
            suggested_activity='yoga',
            suggested_duration_minutes=30,
            difficulty_level='beginner',
            reason='Improve flexibility'
        )
        self.assertEqual(suggestion.user, self.user)
        self.assertEqual(suggestion.suggested_activity, 'yoga')
        self.assertFalse(suggestion.completed)

    def test_mark_suggestion_completed(self):
        """Test marking suggestion as completed"""
        suggestion = WorkoutSuggestion.objects.create(
            user=self.user,
            title='Test Suggestion',
            description='Test',
            suggested_activity='running',
            suggested_duration_minutes=30,
            difficulty_level='beginner',
            reason='Test reason'
        )
        suggestion.completed = True
        suggestion.completed_at = timezone.now()
        suggestion.save()
        
        self.assertTrue(suggestion.completed)
        self.assertIsNotNone(suggestion.completed_at)


class ActivityAPITestCase(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_activity_api(self):
        """Test creating activity via API"""
        data = {
            'activity_type': 'running',
            'title': 'Morning Run',
            'duration_minutes': 30,
            'calories_burned': 300,
            'distance_km': 5.0,
            'activity_date': timezone.now().isoformat()
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)

    def test_list_activities_api(self):
        """Test listing activities via API"""
        Activity.objects.create(
            user=self.user,
            activity_type='running',
            title='Run',
            duration_minutes=30,
            calories_burned=300,
            activity_date=timezone.now()
        )
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_weekly_activities(self):
        """Test getting weekly activities"""
        Activity.objects.create(
            user=self.user,
            activity_type='running',
            title='Run',
            duration_minutes=30,
            calories_burned=300,
            activity_date=timezone.now()
        )
        response = self.client.get('/api/activities/this_week/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_activity_stats(self):
        """Test getting activity statistics"""
        Activity.objects.create(
            user=self.user,
            activity_type='running',
            title='Run',
            duration_minutes=30,
            calories_burned=300,
            distance_km=5.0,
            activity_date=timezone.now()
        )
        response = self.client.get('/api/activities/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_activities'], 1)
        self.assertEqual(response.data['total_calories'], 300)
