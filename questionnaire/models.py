"""Models for the AWFM Questionnaire application."""
from django.db import models


class MainScreenQuestion(models.Model):
    """The main screen question content (singleton)."""
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=200)
    section_label = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Main Screen Question"
        verbose_name_plural = "Main Screen Question"

    def __str__(self):
        return self.title[:50]


class Question(models.Model):
    """A checkpoint question (e.g., Checkpoint 1, 2, 3)."""
    key = models.CharField(max_length=10, unique=True)  # q1, q2, q3
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=200)
    checkpoint_label = models.CharField(max_length=200)
    instruction = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.subtitle}: {self.title}"


class Choice(models.Model):
    """A selectable choice within a question/checkpoint."""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_id = models.CharField(max_length=20)  # q1_1, q1_2, etc.
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500)
    image = models.URLField(blank=True)
    description = models.TextField()

    # Checkpoint 1 (Q1) extended content fields
    why_this_matters = models.TextField(blank=True)
    research_evidence = models.TextField(blank=True)
    decision_impact = models.TextField(blank=True)

    # Checkpoint 2 (Q2) extended content fields
    what_you_are_fighting_for = models.TextField(blank=True)
    cooperative_learning = models.TextField(blank=True)
    barriers_to_access = models.TextField(blank=True)

    # Checkpoint 3 (Q3) extended content fields
    care_team_affirmation = models.TextField(blank=True)
    interdependency_at_work = models.TextField(blank=True)
    reflection_guidance = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['question', 'choice_id']

    def __str__(self):
        return f"{self.question.key} - {self.title[:50]}"


class TeamMember(models.Model):
    """A member of the care team."""
    name = models.CharField(max_length=200)
    avatar = models.URLField(blank=True)
    affirmed = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Response(models.Model):
    """User response to a question."""
    user_id = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    selected_choices = models.ManyToManyField(Choice, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user_id', 'question']

    def __str__(self):
        return f"Response by {self.user_id} to {self.question}"
