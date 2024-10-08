"""sweat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers


from sweatapi.views.auth import check_user, register_user
from sweatapi.views.user import UserView
from sweatapi.views.profile_views import ProfileViewSet
from sweatapi.views.reflections_views import ReflectionViewSet
from sweatapi.views.type_views import TypeViewSet
from sweatapi.views.workout_type_views import WorkoutTypeViewSet
from sweatapi.views.workout_views import WorkoutViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, 'user')
router.register(r'profiles', ProfileViewSet, 'profile')
router.register(r'reflections', ReflectionViewSet, 'reflection')
router.register(r'types', TypeViewSet, 'type')
router.register(r'workouttypes', WorkoutTypeViewSet, 'workouttype')
router.register(r'workouts', WorkoutViewSet, 'workout')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
     path('register', register_user),
    path('checkuser', check_user),
]
