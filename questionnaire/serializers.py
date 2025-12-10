"""Serializers for the AWFM Questionnaire API."""
from rest_framework import serializers
from .models import Question, Choice, TeamMember, MainScreenQuestion, Response


class ChoiceSerializer(serializers.ModelSerializer):
    """Serializer for choices - maps Django field names to camelCase for frontend."""
    id = serializers.CharField(source='choice_id')
    whyThisMatters = serializers.CharField(source='why_this_matters', allow_blank=True)
    researchEvidence = serializers.CharField(source='research_evidence', allow_blank=True)
    decisionImpact = serializers.CharField(source='decision_impact', allow_blank=True)
    whatYouAreFightingFor = serializers.CharField(source='what_you_are_fighting_for', allow_blank=True)
    cooperativeLearning = serializers.CharField(source='cooperative_learning', allow_blank=True)
    barriersToAccess = serializers.CharField(source='barriers_to_access', allow_blank=True)
    careTeamAffirmation = serializers.CharField(source='care_team_affirmation', allow_blank=True)
    interdependencyAtWork = serializers.CharField(source='interdependency_at_work', allow_blank=True)
    reflectionGuidance = serializers.CharField(source='reflection_guidance', allow_blank=True)

    class Meta:
        model = Choice
        fields = [
            'id', 'title', 'subtitle', 'image', 'description',
            'whyThisMatters', 'researchEvidence', 'decisionImpact',
            'whatYouAreFightingFor', 'cooperativeLearning', 'barriersToAccess',
            'careTeamAffirmation', 'interdependencyAtWork', 'reflectionGuidance'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for question metadata."""
    checkpointLabel = serializers.CharField(source='checkpoint_label')

    class Meta:
        model = Question
        fields = ['title', 'subtitle', 'checkpointLabel', 'instruction']


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'avatar', 'affirmed']


class MainScreenQuestionSerializer(serializers.ModelSerializer):
    sectionLabel = serializers.CharField(source='section_label')

    class Meta:
        model = MainScreenQuestion
        fields = ['title', 'subtitle', 'sectionLabel']


class ResponseSerializer(serializers.ModelSerializer):
    selected_choice_ids = serializers.PrimaryKeyRelatedField(
        queryset=Choice.objects.all(),
        many=True,
        source='selected_choices',
        required=False
    )

    class Meta:
        model = Response
        fields = ['id', 'user_id', 'question', 'selected_choice_ids', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
