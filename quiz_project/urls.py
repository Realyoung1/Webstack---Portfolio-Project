"""
URL configuration for quiz_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views
from quiz_app import views
from quiz_app.views import quiz_list,take_quiz,quiz_score

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from quiz_app.api import QuizViewSet  


router = DefaultRouter()
router.register(r'quizzes', QuizViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    
    #Quiz Urls
    path('quiz_list/', quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/score/', quiz_score, name='quiz_score'),
    #ApI route Path
    path('/api', include(router.urls)),
    
]




