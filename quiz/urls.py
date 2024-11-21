from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, QuestionViewSet, QuizAttemptViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'attempts', QuizAttemptViewSet, basename='attempt')

urlpatterns = [
    path('', include(router.urls)),
]