# SmartFit API Documentation

This document provides comprehensive documentation for the SmartFit API endpoints.

## Table of Contents

1. [Authentication](#authentication)
2. [User Management](#user-management)
3. [Diet Plans](#diet-plans)
4. [Workout Plans](#workout-plans)
5. [Video Tutorials](#video-tutorials)
6. [Video Library](#video-library)
7. [Body Measurements](#body-measurements)
8. [Recipe Library](#recipe-library)
9. [Shopping](#shopping)
10. [Contact Forms](#contact-forms)
11. [Error Handling](#error-handling)
12. [Pagination](#pagination)

## Authentication

### Get Authentication Token

Obtain a JWT token for authenticating API requests.

- **URL**: `/api/token/`
- **Method**: `POST`
- **Auth Required**: No
- **Permissions**: None

**Request Body**:

```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Refresh Token

Refresh an expired JWT token.

- **URL**: `/api/token/refresh/`
- **Method**: `POST`
- **Auth Required**: No
- **Permissions**: None

**Request Body**:

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## User Management

### Register User

Register a new user account.

- **URL**: `/api/register/`
- **Method**: `POST`
- **Auth Required**: No
- **Permissions**: None

**Request Body**:

```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "secure_password",
  "password2": "secure_password"
}
```

**Success Response**:

- **Code**: 201 Created
- **Content**:

```json
{
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "is_active": true,
    "date_joined": "2023-05-17T10:30:45Z"
  }
}
```

### Get User Profile

Retrieve the current user's profile information.

- **URL**: `/api/profile/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Profile retrieved successfully",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "profile": {
      "id": 1,
      "image": "http://example.com/media/profiles/user1.jpg",
      "age": 30,
      "gender": "M",
      "gender_display": "Male",
      "fitness_goal": "WL",
      "fitness_goal_display": "Weight Loss",
      "diet_plan": 2,
      "diet_plan_details": {
        "id": 2,
        "name": "Keto Diet",
        "description": "High fat, low carb diet",
        "image": "http://example.com/media/diet_plans/keto.jpg"
      },
      "workout_plan": 3,
      "workout_plan_details": {
        "id": 3,
        "name": "Full Body Workout",
        "description": "Complete body workout for beginners",
        "image": "http://example.com/media/workout_plans/fullbody.jpg"
      },
      "height": 175,
      "weight": 75,
      "waist_circumference": 85,
      "hip_circumference": 95,
      "chest_circumference": 100,
      "arm_circumference": 35,
      "thigh_circumference": 55,
      "neck_circumference": 40,
      "body_photo": "http://example.com/media/body_measurements/user1.jpg",
      "created_at": "2023-05-17T10:30:45Z",
      "updated_at": "2023-05-17T10:30:45Z"
    }
  }
}
```

### Update User Profile

Update the current user's profile information.

- **URL**: `/api/profile/update/`
- **Method**: `PATCH`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Request Body**:

```json
{
  "name": "John Smith",
  "profile": {
    "age": 31,
    "gender": "M",
    "fitness_goal": "MG",
    "diet_plan": 3,
    "workout_plan": 2,
    "image": "profile_image.jpg"
  }
}
```

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Profile updated successfully",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Smith",
    "profile": {
      "id": 1,
      "image": "http://example.com/media/profiles/profile_image.jpg",
      "age": 31,
      "gender": "M",
      "gender_display": "Male",
      "fitness_goal": "MG",
      "fitness_goal_display": "Muscle Gain",
      "diet_plan": 3,
      "workout_plan": 2
    }
  }
}
```

### Change Password

Change the current user's password.

- **URL**: `/api/change-password/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Request Body**:

```json
{
  "old_password": "current_password",
  "new_password": "new_secure_password",
  "confirm_password": "new_secure_password"
}
```

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Password changed successfully"
}
```

## Workout Plans

### List Workout Plans

Retrieve a list of all available workout plans.

- **URL**: `/workouts/api/plans/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Permissions**: Authenticated User
- **Query Parameters**:
  - `category`: Filter by category (e.g., "ST" for Strength)
  - `difficulty`: Filter by difficulty (e.g., "BG" for Beginner)
  - `featured`: Filter featured plans (e.g., "true")

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Workout plans retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "Full Body Workout",
      "description": "Complete body workout for beginners",
      "category": "ST",
      "category_display": "Strength",
      "difficulty": "BG",
      "difficulty_display": "Beginner",
      "duration_weeks": 4,
      "sessions_per_week": 3,
      "minutes_per_session": 45,
      "image": "http://example.com/media/workout_plans/fullbody.jpg",
      "days_count": 12,
      "is_featured": true,
      "is_active": true,
      "created_at": "2023-05-17T10:30:45Z"
    }
  ]
}
```

### Get Workout Plan Details

Retrieve detailed information about a specific workout plan.

- **URL**: `/workouts/api/plans/{plan_id}/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Workout plan details retrieved successfully",
  "data": {
    "id": 1,
    "name": "Full Body Workout",
    "description": "Complete body workout for beginners",
    "category": "ST",
    "category_display": "Strength",
    "difficulty": "BG",
    "difficulty_display": "Beginner",
    "duration_weeks": 4,
    "sessions_per_week": 3,
    "minutes_per_session": 45,
    "goal": "Build overall strength and improve fitness",
    "image": "http://example.com/media/workout_plans/fullbody.jpg",
    "days": [
      {
        "id": 1,
        "day_number": 1,
        "name": "Day 1 - Upper Body",
        "description": "Focus on chest, shoulders, and arms",
        "rest_day": false,
        "exercises": [
          {
            "id": 1,
            "exercise": {
              "id": 1,
              "name": "Push-ups",
              "description": "Basic push-up exercise",
              "body_part": "CH",
              "body_part_display": "Chest",
              "difficulty": "BG",
              "difficulty_display": "Beginner",
              "instructions": "Start in plank position and lower your body...",
              "tips": "Keep your core tight throughout the movement",
              "image": "http://example.com/media/exercises/pushup.jpg",
              "video_url": "http://example.com/videos/pushup.mp4",
              "equipment_needed": "NO",
              "equipment_description": "No equipment needed"
            },
            "order": 1,
            "sets": 3,
            "reps": 10,
            "rest_seconds": 60,
            "notes": "Modify with knee push-ups if needed"
          }
        ]
      }
    ],
    "video_tutorials": [
      {
        "id": 1,
        "title": "How to do proper push-ups",
        "description": "Learn the correct form for push-ups",
        "video_url": "http://example.com/videos/pushup_tutorial.mp4",
        "duration_minutes": 5,
        "duration_seconds": 30,
        "duration_display": "5:30",
        "thumbnail": "http://example.com/media/thumbnails/pushup.jpg",
        "order": 1,
        "is_featured": true,
        "is_active": true
      }
    ],
    "is_featured": true,
    "is_active": true,
    "created_at": "2023-05-17T10:30:45Z",
    "updated_at": "2023-05-17T10:30:45Z"
  }
}
```

### List User Workouts

Retrieve a list of the user's selected workout plans.

- **URL**: `/workouts/api/my-workouts/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Your workout plans retrieved successfully",
  "data": [
    {
      "id": 1,
      "workout_plan": {
        "id": 1,
        "name": "Full Body Workout",
        "description": "Complete body workout for beginners",
        "category": "ST",
        "category_display": "Strength",
        "difficulty": "BG",
        "difficulty_display": "Beginner",
        "image": "http://example.com/media/workout_plans/fullbody.jpg"
      },
      "start_date": "2023-05-17",
      "is_active": true,
      "completed": false,
      "notes": "Starting this program to build strength",
      "created_at": "2023-05-17T10:30:45Z",
      "updated_at": "2023-05-17T10:30:45Z"
    }
  ]
}
```

### Select Workout Plan

Select a workout plan for the user.

- **URL**: `/workouts/api/select-plan/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Request Body**:

```json
{
  "workout_plan_id": 1
}
```

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "You have successfully selected the \"Full Body Workout\" workout plan",
  "data": {
    "id": 1,
    "workout_plan": {
      "id": 1,
      "name": "Full Body Workout",
      "description": "Complete body workout for beginners"
    },
    "start_date": "2023-05-17",
    "is_active": true,
    "completed": false,
    "notes": "",
    "created_at": "2023-05-17T10:30:45Z",
    "updated_at": "2023-05-17T10:30:45Z"
  }
}
```

## Video Tutorials

### List Video Tutorials for a Workout Plan

Retrieve a list of video tutorials for a specific workout plan.

- **URL**: `/workouts/api/plans/{workout_plan_id}/videos/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Permissions**: Authenticated User
- **Query Parameters**:
  - `featured`: Filter featured videos (e.g., "true")

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Video tutorials retrieved successfully",
  "data": [
    {
      "id": 1,
      "title": "How to do proper push-ups",
      "description": "Learn the correct form for push-ups",
      "video_url": "http://example.com/videos/pushup_tutorial.mp4",
      "duration_minutes": 5,
      "duration_seconds": 30,
      "duration_display": "5:30",
      "thumbnail": "http://example.com/media/thumbnails/pushup.jpg",
      "order": 1,
      "is_featured": true,
      "is_active": true,
      "created_at": "2023-05-17T10:30:45Z",
      "updated_at": "2023-05-17T10:30:45Z"
    }
  ]
}
```

### Get Video Tutorial Details

Retrieve detailed information about a specific video tutorial.

- **URL**: `/workouts/api/videos/{video_id}/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Video tutorial details retrieved successfully",
  "data": {
    "id": 1,
    "title": "How to do proper push-ups",
    "description": "Learn the correct form for push-ups",
    "video_url": "http://example.com/videos/pushup_tutorial.mp4",
    "duration_minutes": 5,
    "duration_seconds": 30,
    "duration_display": "5:30",
    "thumbnail": "http://example.com/media/thumbnails/pushup.jpg",
    "order": 1,
    "is_featured": true,
    "is_active": true,
    "created_at": "2023-05-17T10:30:45Z",
    "updated_at": "2023-05-17T10:30:45Z"
  }
}
```

## Video Library

### List User's Video Library

Retrieve a list of videos in the user's library.

- **URL**: `/workouts/api/video-library/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Permissions**: Authenticated User
- **Query Parameters**:
  - `category`: Filter by category (e.g., "WO" for Workout)
  - `favorites`: Filter favorite videos (e.g., "true")
  - `source_type`: Filter by source type (e.g., "tutorial")
  - `search`: Search by title or description
  - `ordering`: Order results (e.g., "created_at", "-created_at", "title")

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Your video library retrieved successfully",
  "data": [
    {
      "id": 1,
      "title": "How to do proper push-ups",
      "description": "Learn the correct form for push-ups",
      "video_url": "http://example.com/videos/pushup_tutorial.mp4",
      "category": "WO",
      "category_display": "Workout",
      "duration_minutes": 5,
      "duration_seconds": 30,
      "duration_display": "5:30",
      "thumbnail": "http://example.com/media/thumbnails/pushup.jpg",
      "is_favorite": true,
      "notes": "Great tutorial for beginners",
      "source_type": "tutorial",
      "source_type_display": "Workout Tutorial",
      "source_id": 1,
      "created_at": "2023-05-17T10:30:45Z",
      "updated_at": "2023-05-17T10:30:45Z"
    }
  ]
}
```

### Add Video to Library

Add a new video to the user's library.

- **URL**: `/workouts/api/video-library/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Request Body**:

```json
{
  "title": "Healthy Meal Prep Ideas",
  "description": "Quick and easy meal prep ideas for the week",
  "video_url": "http://example.com/videos/meal_prep.mp4",
  "category": "NU",
  "duration_minutes": 10,
  "duration_seconds": 15,
  "thumbnail": "meal_prep_thumbnail.jpg",
  "is_favorite": false,
  "notes": "Good for weekly meal planning",
  "source_type": "external"
}
```

**Success Response**:

- **Code**: 201 Created
- **Content**:

```json
{
  "message": "Video saved to your library successfully",
  "data": {
    "id": 2,
    "title": "Healthy Meal Prep Ideas",
    "description": "Quick and easy meal prep ideas for the week",
    "video_url": "http://example.com/videos/meal_prep.mp4",
    "category": "NU",
    "category_display": "Nutrition",
    "duration_minutes": 10,
    "duration_seconds": 15,
    "duration_display": "10:15",
    "thumbnail": "http://example.com/media/thumbnails/meal_prep_thumbnail.jpg",
    "is_favorite": false,
    "notes": "Good for weekly meal planning",
    "source_type": "external",
    "source_type_display": "External Video",
    "source_id": null,
    "created_at": "2023-05-17T10:30:45Z",
    "updated_at": "2023-05-17T10:30:45Z"
  }
}
```

### Get Saved Video Details

Retrieve detailed information about a specific saved video.

- **URL**: `/workouts/api/video-library/{video_id}/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Saved video details retrieved successfully",
  "data": {
    "id": 1,
    "title": "How to do proper push-ups",
    "description": "Learn the correct form for push-ups",
    "video_url": "http://example.com/videos/pushup_tutorial.mp4",
    "category": "WO",
    "category_display": "Workout",
    "duration_minutes": 5,
    "duration_seconds": 30,
    "duration_display": "5:30",
    "thumbnail": "http://example.com/media/thumbnails/pushup.jpg",
    "is_favorite": true,
    "notes": "Great tutorial for beginners",
    "source_type": "tutorial",
    "source_type_display": "Workout Tutorial",
    "source_id": 1,
    "created_at": "2023-05-17T10:30:45Z",
    "updated_at": "2023-05-17T10:30:45Z"
  }
}
```

### Update Saved Video

Update information about a saved video.

- **URL**: `/workouts/api/video-library/{video_id}/`
- **Method**: `PATCH`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Request Body**:

```json
{
  "title": "Updated Video Title",
  "notes": "Added some personal notes",
  "is_favorite": true
}
```

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Saved video updated successfully",
  "data": {
    "id": 1,
    "title": "Updated Video Title",
    "description": "Learn the correct form for push-ups",
    "video_url": "http://example.com/videos/pushup_tutorial.mp4",
    "category": "WO",
    "category_display": "Workout",
    "duration_minutes": 5,
    "duration_seconds": 30,
    "duration_display": "5:30",
    "thumbnail": "http://example.com/media/thumbnails/pushup.jpg",
    "is_favorite": true,
    "notes": "Added some personal notes",
    "source_type": "tutorial",
    "source_type_display": "Workout Tutorial",
    "source_id": 1,
    "created_at": "2023-05-17T10:30:45Z",
    "updated_at": "2023-05-17T10:30:45Z"
  }
}
```

### Delete Saved Video

Remove a video from the user's library.

- **URL**: `/workouts/api/video-library/{video_id}/`
- **Method**: `DELETE`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Success Response**:

- **Code**: 204 No Content
- **Content**:

```json
{
  "message": "Video removed from your library successfully"
}
```

### Save Tutorial to Library

Save a workout tutorial video to the user's library.

- **URL**: `/workouts/api/video-library/save-tutorial/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Request Body**:

```json
{
  "tutorial_id": 1
}
```

**Success Response**:

- **Code**: 201 Created
- **Content**:

```json
{
  "message": "Tutorial saved to your library successfully",
  "data": {
    "id": 3,
    "title": "How to do proper push-ups",
    "description": "Learn the correct form for push-ups",
    "video_url": "http://example.com/videos/pushup_tutorial.mp4",
    "category": "WO",
    "category_display": "Workout",
    "duration_minutes": 5,
    "duration_seconds": 30,
    "duration_display": "5:30",
    "thumbnail": "http://example.com/media/thumbnails/pushup.jpg",
    "is_favorite": false,
    "notes": null,
    "source_type": "tutorial",
    "source_type_display": "Workout Tutorial",
    "source_id": 1,
    "created_at": "2023-05-17T10:30:45Z",
    "updated_at": "2023-05-17T10:30:45Z"
  }
}
```

### Toggle Favorite Status

Toggle the favorite status of a saved video.

- **URL**: `/workouts/api/video-library/{video_id}/toggle-favorite/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Video added to favorites successfully",
  "data": {
    "id": 1,
    "title": "How to do proper push-ups",
    "description": "Learn the correct form for push-ups",
    "video_url": "http://example.com/videos/pushup_tutorial.mp4",
    "category": "WO",
    "category_display": "Workout",
    "duration_minutes": 5,
    "duration_seconds": 30,
    "duration_display": "5:30",
    "thumbnail": "http://example.com/media/thumbnails/pushup.jpg",
    "is_favorite": true,
    "notes": "Great tutorial for beginners",
    "source_type": "tutorial",
    "source_type_display": "Workout Tutorial",
    "source_id": 1,
    "created_at": "2023-05-17T10:30:45Z",
    "updated_at": "2023-05-17T10:30:45Z"
  }
}
```

## Diet Plans

### List Diet Plans

Retrieve a list of all available diet plans.

- **URL**: `/diet-plans/api/plans/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Permissions**: Authenticated User
- **Query Parameters**:
  - `category`: Filter by category (e.g., "KT" for Keto)
  - `featured`: Filter featured plans (e.g., "true")

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Diet plans retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "Keto Diet",
      "description": "High fat, low carb diet",
      "category": "KT",
      "category_display": "Keto",
      "duration_weeks": 4,
      "image": "http://example.com/media/diet_plans/keto.jpg",
      "is_featured": true,
      "is_active": true,
      "created_at": "2023-05-17T10:30:45Z"
    }
  ]
}
```

### Get Diet Plan Details

Retrieve detailed information about a specific diet plan.

- **URL**: `/diet-plans/api/plans/{plan_id}/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Diet plan details retrieved successfully",
  "data": {
    "id": 1,
    "name": "Keto Diet",
    "description": "High fat, low carb diet",
    "category": "KT",
    "category_display": "Keto",
    "duration_weeks": 4,
    "calories_per_day": 1800,
    "protein_percentage": 25,
    "carbs_percentage": 5,
    "fat_percentage": 70,
    "recommended_foods": "Meat, fish, eggs, dairy, nuts, healthy oils",
    "foods_to_avoid": "Sugar, grains, beans, root vegetables, fruits",
    "image": "http://example.com/media/diet_plans/keto.jpg",
    "meal_plans": [
      {
        "id": 1,
        "day": 1,
        "meals": [
          {
            "id": 1,
            "meal_type": "BF",
            "meal_type_display": "Breakfast",
            "name": "Avocado and Egg Bowl",
            "description": "Avocado bowl with fried eggs and bacon",
            "calories": 450,
            "protein": 25,
            "carbs": 5,
            "fat": 35,
            "recipe_link": "http://example.com/recipes/avocado-egg-bowl",
            "image": "http://example.com/media/meals/avocado-egg.jpg"
          }
        ]
      }
    ],
    "is_featured": true,
    "is_active": true,
    "created_at": "2023-05-17T10:30:45Z",
    "updated_at": "2023-05-17T10:30:45Z"
  }
}
```

### Select Diet Plan

Select a diet plan for the user.

- **URL**: `/diet-plans/api/select-plan/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Request Body**:

```json
{
  "diet_plan_id": 1
}
```

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "You have successfully selected the \"Keto Diet\" diet plan",
  "data": {
    "id": 1,
    "name": "Keto Diet",
    "description": "High fat, low carb diet",
    "category": "KT",
    "category_display": "Keto",
    "image": "http://example.com/media/diet_plans/keto.jpg"
  }
}
```

## Body Measurements

### Update Body Measurements

Update the user's body measurements.

- **URL**: `/api/profile/update-measurements/`
- **Method**: `PATCH`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Request Body**:

```json
{
  "height": 175,
  "weight": 75,
  "waist_circumference": 85,
  "hip_circumference": 95,
  "chest_circumference": 100,
  "arm_circumference": 35,
  "thigh_circumference": 55,
  "neck_circumference": 40,
  "body_photo": "body_photo.jpg"
}
```

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Body measurements updated successfully",
  "data": {
    "height": 175,
    "weight": 75,
    "waist_circumference": 85,
    "hip_circumference": 95,
    "chest_circumference": 100,
    "arm_circumference": 35,
    "thigh_circumference": 55,
    "neck_circumference": 40,
    "body_photo": "http://example.com/media/body_measurements/body_photo.jpg"
  }
}
```

## Recipe Library

### List Recipes

Retrieve a list of all available recipes.

- **URL**: `/recipes/api/recipes/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Permissions**: Authenticated User
- **Query Parameters**:
  - `category`: Filter by category (e.g., "BF" for Breakfast)
  - `diet_type`: Filter by diet type (e.g., "KT" for Keto)
  - `featured`: Filter featured recipes (e.g., "true")
  - `search`: Search by title or description

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Recipes retrieved successfully",
  "data": [
    {
      "id": 1,
      "title": "Avocado and Egg Bowl",
      "description": "Avocado bowl with fried eggs and bacon",
      "category": "BF",
      "category_display": "Breakfast",
      "diet_type": "KT",
      "diet_type_display": "Keto",
      "prep_time_minutes": 10,
      "cook_time_minutes": 15,
      "calories": 450,
      "protein": 25,
      "carbs": 5,
      "fat": 35,
      "image": "http://example.com/media/recipes/avocado-egg.jpg",
      "is_featured": true,
      "is_active": true,
      "created_at": "2023-05-17T10:30:45Z"
    }
  ]
}
```

### Get Recipe Details

Retrieve detailed information about a specific recipe.

- **URL**: `/recipes/api/recipes/{recipe_id}/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Recipe details retrieved successfully",
  "data": {
    "id": 1,
    "title": "Avocado and Egg Bowl",
    "description": "Avocado bowl with fried eggs and bacon",
    "category": "BF",
    "category_display": "Breakfast",
    "diet_type": "KT",
    "diet_type_display": "Keto",
    "prep_time_minutes": 10,
    "cook_time_minutes": 15,
    "servings": 1,
    "calories": 450,
    "protein": 25,
    "carbs": 5,
    "fat": 35,
    "ingredients": [
      "1 ripe avocado",
      "2 large eggs",
      "2 strips of bacon",
      "Salt and pepper to taste"
    ],
    "instructions": "1. Cook bacon until crispy\n2. Fry eggs\n3. Slice avocado\n4. Combine in a bowl",
    "tips": "For extra flavor, add hot sauce or fresh herbs",
    "image": "http://example.com/media/recipes/avocado-egg.jpg",
    "video_url": "http://example.com/videos/avocado-egg-recipe.mp4",
    "is_featured": true,
    "is_active": true,
    "created_at": "2023-05-17T10:30:45Z",
    "updated_at": "2023-05-17T10:30:45Z"
  }
}
```

## Shopping

### List Products

Retrieve a list of all available products.

- **URL**: `/shop/api/products/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Permissions**: Authenticated User
- **Query Parameters**:
  - `category`: Filter by category (e.g., "SP" for Supplements)
  - `featured`: Filter featured products (e.g., "true")
  - `search`: Search by name or description
  - `min_price`: Filter by minimum price
  - `max_price`: Filter by maximum price

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Products retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "Protein Powder",
      "description": "High-quality whey protein powder",
      "category": "SP",
      "category_display": "Supplements",
      "price": 29.99,
      "discount_price": 24.99,
      "stock": 100,
      "image": "http://example.com/media/products/protein.jpg",
      "is_featured": true,
      "is_active": true,
      "created_at": "2023-05-17T10:30:45Z"
    }
  ]
}
```

### Get Product Details

Retrieve detailed information about a specific product.

- **URL**: `/shop/api/products/{product_id}/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Product details retrieved successfully",
  "data": {
    "id": 1,
    "name": "Protein Powder",
    "description": "High-quality whey protein powder",
    "category": "SP",
    "category_display": "Supplements",
    "price": 29.99,
    "discount_price": 24.99,
    "stock": 100,
    "details": "20g of protein per serving, low in carbs and fat",
    "ingredients": "Whey protein isolate, natural flavors, stevia",
    "usage_instructions": "Mix one scoop with 8oz of water or milk",
    "image": "http://example.com/media/products/protein.jpg",
    "is_featured": true,
    "is_active": true,
    "created_at": "2023-05-17T10:30:45Z",
    "updated_at": "2023-05-17T10:30:45Z"
  }
}
```

### Add to Cart

Add a product to the user's shopping cart.

- **URL**: `/shop/api/cart/add/`
- **Method**: `POST`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Request Body**:

```json
{
  "product_id": 1,
  "quantity": 2
}
```

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Product added to cart successfully",
  "data": {
    "id": 1,
    "items": [
      {
        "id": 1,
        "product": {
          "id": 1,
          "name": "Protein Powder",
          "price": 29.99,
          "discount_price": 24.99,
          "image": "http://example.com/media/products/protein.jpg"
        },
        "quantity": 2,
        "total": 49.98
      }
    ],
    "total_items": 2,
    "subtotal": 49.98,
    "total": 49.98
  }
}
```

### View Cart

Retrieve the user's shopping cart.

- **URL**: `/shop/api/cart/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Permissions**: Authenticated User

**Success Response**:

- **Code**: 200 OK
- **Content**:

```json
{
  "message": "Cart retrieved successfully",
  "data": {
    "id": 1,
    "items": [
      {
        "id": 1,
        "product": {
          "id": 1,
          "name": "Protein Powder",
          "price": 29.99,
          "discount_price": 24.99,
          "image": "http://example.com/media/products/protein.jpg"
        },
        "quantity": 2,
        "total": 49.98
      }
    ],
    "total_items": 2,
    "subtotal": 49.98,
    "total": 49.98
  }
}
```

## Contact Forms

### Submit Contact Form

Submit a contact form.

- **URL**: `/forms/api/contact/`
- **Method**: `POST`
- **Auth Required**: No
- **Permissions**: None

**Request Body**:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "query_type": "GQ",
  "message": "I have a question about the SmartFit app."
}
```

**Success Response**:

- **Code**: 201 Created
- **Content**:

```json
{
  "message": "Contact form submitted successfully",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "query_type": "GQ",
    "query_type_display": "General Query",
    "message": "I have a question about the SmartFit app.",
    "created_at": "2023-05-17T10:30:45Z"
  }
}
```

### Subscribe to Newsletter

Subscribe to the newsletter.

- **URL**: `/forms/api/newsletter/`
- **Method**: `POST`
- **Auth Required**: No
- **Permissions**: None

**Request Body**:

```json
{
  "email": "john@example.com"
}
```

**Success Response**:

- **Code**: 201 Created
- **Content**:

```json
{
  "message": "Subscribed to newsletter successfully",
  "data": {
    "id": 1,
    "email": "john@example.com",
    "created_at": "2023-05-17T10:30:45Z"
  }
}
```

## Error Handling

All API endpoints follow a consistent error handling pattern. When an error occurs, the API returns an appropriate HTTP status code along with a JSON response containing error details.

### Common Error Codes

- **400 Bad Request**: The request was invalid or cannot be served. The exact error is specified in the response.
- **401 Unauthorized**: Authentication credentials were missing or invalid.
- **403 Forbidden**: The authenticated user does not have permission to access the requested resource.
- **404 Not Found**: The requested resource does not exist.
- **405 Method Not Allowed**: The HTTP method used is not supported for this resource.
- **500 Internal Server Error**: An error occurred on the server.

### Error Response Format

```json
{
  "error": "Detailed error message",
  "code": "ERROR_CODE"
}
```

### Validation Errors

For validation errors, the response includes field-specific error messages:

```json
{
  "error": "Validation error",
  "fields": {
    "email": ["This field is required."],
    "password": ["Password must be at least 8 characters long."]
  }
}
```

## Pagination

For endpoints that return lists of items, pagination is supported using limit and offset parameters.

### Pagination Parameters

- `limit`: Number of items to return (default: 10, max: 100)
- `offset`: Number of items to skip (default: 0)

### Paginated Response Format

```json
{
  "message": "Resources retrieved successfully",
  "data": [...],
  "pagination": {
    "count": 100,
    "next": "http://example.com/api/resources/?limit=10&offset=10",
    "previous": null,
    "limit": 10,
    "offset": 0
  }
}
```
