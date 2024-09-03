Project Overview
Name: Sweat

Purpose: A fitness-related application where users can track their workouts, workout types, and other related data. It integrates with Django and Django REST Framework for backend management and provides various functionalities related to workouts and workout types.

Key Models:

User: Represents the users of the application.
Profile: Extends user information with details like age, gender, weight, height, and fitness goals.
Workout: Records individual workout sessions, including fields for date, duration, intensity, and the type of workout.
WorkoutType: Connects workouts with specific types of exercises, with a foreign key to Workout and Type.
Type: Defines different workout types (e.g., cardio, strength training).

API Endpoints:
/workouttypes: Manages the creation and retrieval of workout types. The POST method allows creating new workout types, while GET retrieves existing ones.
/workouts: manages the creation, retrieval, updating, and deletion of individual workouts.
## Postman Documentation
You can view the Postman documentation for this project [here](https://documenter.getpostman.com/view/29817482/2sAXjNYAxM).


Key Features:
CRUD Operations: Create, read, update, and delete operations for WorkoutType and Workout.
Relationships:
WorkoutType links to Workout and Type.
Workout contains data about the exercise session and links to WorkoutType.
Profile links to User and stores additional details.

Technical Stack:
Backend Framework: Django
REST API Framework: Django REST Framework

User Description:

The primary user of the Sweat project is an individual who is committed to maintaining and improving their fitness levels through regular workouts. They are health-conscious and seek to track their exercise routines systematically to monitor progress and make data-driven decisions about their fitness regimen.

Profile Characteristics:
Personal Information:

Age: Users vary in age, with profiles capturing this detail to help tailor workout recommendations.
Gender: The system supports multiple genders, enabling personalized fitness tracking.
Weight and Height: These metrics are used to calculate fitness-related statistics and monitor changes over time.
Fitness Goals: Users can set and track personal fitness goals, such as weight loss, muscle gain, or endurance improvement.
Workout Enthusiasts:

Variety of Workouts: Users engage in different types of workouts, from cardio and strength training to flexibility exercises.
Detailed Tracking: They appreciate detailed tracking of workouts, including duration, intensity, and specific workout types.
Motivation and Engagement:

Goal-Oriented: Users are motivated by achieving fitness goals and tracking their progress.
Data-Driven Decisions: They use data from their workouts to adjust their routines and improve performance.
Technologically Savvy:

Comfort with Technology: Users are comfortable using web applications and APIs to manage and track their fitness data.
Utilizes Online Tools: They leverage online tools for detailed workout tracking and goal setting.
Community and Support:

Social Aspects: Users might be interested in sharing their progress or participating in fitness communities for additional support and motivation.
User Needs:
Efficient Tracking: A system that allows them to log workouts quickly and accurately.
Personalization: Customizable features to accommodate different workout types and fitness goals.
Progress Monitoring: Tools to monitor progress over time, including visualizations and detailed reports.
Error-Free Data Handling: Reliable data entry and retrieval without errors to ensure accurate tracking and reporting.
Overall, the Sweat project is designed to cater to users who are dedicated to their fitness journey and seek a reliable, user-friendly platform to support their workout and health goals.
