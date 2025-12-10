"""URL configuration for the questionnaire API."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'responses', views.ResponseViewSet)
router.register(r'team', views.TeamMemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('main-question/', views.MainScreenQuestionView.as_view(), name='main-question'),
    path('questions/', views.QuestionDataView.as_view(), name='question-data'),
    path('choices/<str:question_key>/', views.ChoicesView.as_view(), name='choices'),
    path('health/', views.health_check, name='health-check'),
]
