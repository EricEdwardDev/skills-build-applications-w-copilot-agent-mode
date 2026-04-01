"""
Django settings configuration for octofit_tracker app.
This file contains app-level settings and configurations.
"""

import os

# Codespace configuration for Django
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
if os.environ.get('CODESPACE_NAME'):
    ALLOWED_HOSTS.append(f"{os.environ.get('CODESPACE_NAME')}-8000.app.github.dev")

# Database connection settings for MongoDB
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'octofit_db',
        'ENFORCE_SCHEMA_STRUCTURE': False,
        'CLIENT': {
            'host': 'localhost',
            'port': 27017,
        }
    }
}

# Legacy database config
DATABASES_CONFIG = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'octofit_db',
        'ENFORCE_SCHEMA_STRUCTURE': False,
        'CLIENT': {
            'host': 'localhost',
            'port': 27017,
        }
    }
}

# REST Framework Configuration
REST_FRAMEWORK_CONFIG = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

if os.environ.get('CODESPACE_NAME'):
    CORS_ALLOWED_ORIGINS.append(f"https://{os.environ.get('CODESPACE_NAME')}-3000.app.github.dev")

# Activity level choices
ACTIVITY_LEVELS = [
    ('sedentary', 'Sedentary'),
    ('lightly_active', 'Lightly Active'),
    ('moderately_active', 'Moderately Active'),
    ('very_active', 'Very Active'),
    ('extremely_active', 'Extremely Active'),
]

# Activity type choices
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
