from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from octofit_tracker.models import (
    UserProfile, Activity, Team, Leaderboard, WorkoutSuggestion
)


class Command(BaseCommand):
    help = 'Populate OctoFit database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))
        
        # Create test users
        users = []
        usernames = ['alice', 'bob', 'charlie', 'diana', 'evan', 'fiona']
        
        for username in usernames:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': username.capitalize(),
                    'last_name': 'Champion'
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
            users.append(user)

        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(users)} users'))

        # Create user profiles
        activity_levels = ['sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extremely_active']
        for user in users:
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': f'Fitness enthusiast from the OctoFit community',
                    'age': random.randint(20, 50),
                    'height': random.randint(160, 190),
                    'weight': random.randint(60, 100),
                    'activity_level': random.choice(activity_levels),
                    'fitness_goals': 'Lose weight, Build muscle, Improve endurance'
                }
            )

        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(users)} user profiles'))

        # Create teams
        teams_data = [
            {'name': 'Running Rebels', 'description': 'For running enthusiasts'},
            {'name': 'Yoga Warriors', 'description': 'Zen fitness masters'},
            {'name': 'Swimming Sharks', 'description': 'Water sports champions'},
        ]

        teams = []
        for team_data in teams_data:
            team, created = Team.objects.get_or_create(
                name=team_data['name'],
                defaults={
                    'description': team_data['description'],
                    'leader': users[0]
                }
            )
            if created:
                team.members.add(*users)
            teams.append(team)

        self.stdout.write(self.style.SUCCESS(f'✓ Created {len(teams)} teams'))

        # Create activities
        activity_types = ['running', 'cycling', 'swimming', 'walking', 'gym', 'yoga', 'sports']
        activities = 0
        
        for user in users:
            for _ in range(random.randint(3, 8)):
                activity_date = timezone.now() - timedelta(days=random.randint(0, 30))
                duration = random.randint(15, 120)
                
                Activity.objects.get_or_create(
                    user=user,
                    activity_date=activity_date,
                    title=f'{random.choice(activity_types).title()} Session',
                    defaults={
                        'activity_type': random.choice(activity_types),
                        'description': 'Great workout session!',
                        'duration_minutes': duration,
                        'calories_burned': random.randint(100, 800),
                        'distance_km': round(random.uniform(1, 10), 2),
                        'intensity_level': random.choice(['low', 'medium', 'high'])
                    }
                )
                activities += 1

        self.stdout.write(self.style.SUCCESS(f'✓ Created multiple activities'))

        # Create leaderboards for current week
        from datetime import datetime
        now = datetime.now()
        week = now.isocalendar()[1]
        year = now.isocalendar()[0]

        for team in teams:
            for rank, user in enumerate(users, 1):
                total_activities = Activity.objects.filter(user=user).count()
                total_calories = sum(
                    activity.calories_burned 
                    for activity in Activity.objects.filter(user=user)
                )
                
                leaderboard, created = Leaderboard.objects.get_or_create(
                    team=team,
                    user=user,
                    challenge_week=week,
                    challenge_year=year,
                    defaults={
                        'total_calories': total_calories,
                        'total_activities': total_activities,
                        'rank': rank
                    }
                )

        self.stdout.write(self.style.SUCCESS(f'✓ Created leaderboards for current week'))

        # Create workout suggestions
        suggestions_data = [
            {
                'title': 'Morning Run',
                'description': 'Start your day with an energizing run',
                'suggested_activity': 'running',
                'suggested_duration_minutes': 30,
                'difficulty_level': 'intermediate',
                'reason': 'Build cardiovascular endurance'
            },
            {
                'title': 'Yoga Session',
                'description': 'Relax and improve flexibility',
                'suggested_activity': 'yoga',
                'suggested_duration_minutes': 45,
                'difficulty_level': 'beginner',
                'reason': 'Reduce stress and increase flexibility'
            },
            {
                'title': 'Swimming Workout',
                'description': 'Full body workout in the pool',
                'suggested_activity': 'swimming',
                'suggested_duration_minutes': 60,
                'difficulty_level': 'intermediate',
                'reason': 'Low impact, high intensity exercise'
            },
            {
                'title': 'Gym Session',
                'description': 'Strength training workout',
                'suggested_activity': 'gym',
                'suggested_duration_minutes': 60,
                'difficulty_level': 'advanced',
                'reason': 'Build muscle strength'
            },
        ]

        suggestions = 0
        for user in users:
            for suggestion_data in random.sample(suggestions_data, k=2):
                WorkoutSuggestion.objects.get_or_create(
                    user=user,
                    title=suggestion_data['title'],
                    defaults={
                        'description': suggestion_data['description'],
                        'suggested_activity': suggestion_data['suggested_activity'],
                        'suggested_duration_minutes': suggestion_data['suggested_duration_minutes'],
                        'difficulty_level': suggestion_data['difficulty_level'],
                        'reason': suggestion_data['reason'],
                    }
                )
                suggestions += 1

        self.stdout.write(self.style.SUCCESS(f'✓ Created workout suggestions'))

        self.stdout.write(self.style.SUCCESS('✓ Database population completed successfully!'))
        self.stdout.write(self.style.WARNING('\nTest Users:'))
        for username in usernames:
            self.stdout.write(f'  Username: {username}, Password: testpass123')
