"""API views for the AWFM Questionnaire."""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response as DRFResponse
from rest_framework.views import APIView

from .models import Question, Choice, TeamMember, MainScreenQuestion, Response
from .serializers import (
    QuestionSerializer, ChoiceSerializer,
    TeamMemberSerializer, MainScreenQuestionSerializer, ResponseSerializer
)


class MainScreenQuestionView(APIView):
    """Get the main screen question."""
    def get(self, request):
        question = MainScreenQuestion.objects.first()
        if question:
            serializer = MainScreenQuestionSerializer(question)
            return DRFResponse(serializer.data)
        return DRFResponse({
            'title': '',
            'subtitle': '',
            'sectionLabel': ''
        })


class QuestionDataView(APIView):
    """Get question metadata for all checkpoints (q1, q2, q3)."""
    def get(self, request):
        questions = Question.objects.all()
        result = {}
        for q in questions:
            result[q.key] = QuestionSerializer(q).data
        return DRFResponse(result)


class ChoicesView(APIView):
    """Get choices for a specific question (q1, q2, or q3)."""
    def get(self, request, question_key):
        try:
            question = Question.objects.get(key=question_key)
            choices = question.choices.all()
            serializer = ChoiceSerializer(choices, many=True)
            return DRFResponse(serializer.data)
        except Question.DoesNotExist:
            return DRFResponse([], status=status.HTTP_404_NOT_FOUND)


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for team members (with affirmation status)."""
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer


class ResponseViewSet(viewsets.ModelViewSet):
    """API endpoint for user responses."""
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

    def get_queryset(self):
        queryset = Response.objects.all()
        user_id = self.request.query_params.get('user_id')
        question_key = self.request.query_params.get('question')

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if question_key:
            queryset = queryset.filter(question__key=question_key)

        return queryset

    def create(self, request, *args, **kwargs):
        """Create or update a response (upsert behavior)."""
        user_id = request.data.get('user_id')
        question_key = request.data.get('question')

        if user_id and question_key:
            try:
                question = Question.objects.get(key=question_key)
                existing = Response.objects.get(user_id=user_id, question=question)
                serializer = self.get_serializer(existing, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return DRFResponse(serializer.data, status=status.HTTP_200_OK)
            except (Question.DoesNotExist, Response.DoesNotExist):
                pass

        return super().create(request, *args, **kwargs)


@api_view(['GET'])
def health_check(request):
    """Health check endpoint."""
    return DRFResponse({'status': 'healthy', 'service': 'awfm-questionnaire'})
