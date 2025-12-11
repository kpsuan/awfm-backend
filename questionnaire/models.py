"""Models for the AWFM Questionnaire application."""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


# =============================================================================
# USER & AUTHENTICATION
# =============================================================================

class User(AbstractUser):
    """Custom user model for AWFM."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    avatar = models.URLField(blank=True)
    bio = models.TextField(blank=True)

    # Use email as username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


# =============================================================================
# QUESTIONNAIRE STRUCTURE
# =============================================================================

class Section(models.Model):
    """A section grouping multiple questions (e.g., 'ADVANCE CARE PLANNING PART 1')."""
    key = models.CharField(max_length=20, unique=True)  # section_1, section_2, etc.
    title = models.CharField(max_length=300)  # "ADVANCE CARE PLANNING (PART 1)"
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class MainQuestion(models.Model):
    """
    A main question in the questionnaire (e.g., Q10A, Q10B, Q11).
    Each main question has 3 checkpoints.
    """
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='questions')
    key = models.CharField(max_length=20, unique=True)  # q10a, q10b, q11, etc.
    title = models.CharField(max_length=500)  # The actual question text
    subtitle = models.CharField(max_length=300, blank=True)  # e.g., "Question 10 A"
    description = models.TextField(blank=True)  # Additional context
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Main Question"
        verbose_name_plural = "Main Questions"

    def __str__(self):
        return f"{self.key.upper()}: {self.title[:50]}"


class Checkpoint(models.Model):
    """
    A checkpoint within a main question (3 per question).
    e.g., Checkpoint 1: Your Position, Checkpoint 2: Your Challenges, etc.
    """
    CHECKPOINT_TYPES = [
        ('position', 'Your Position'),
        ('challenges', 'Your Challenges'),
        ('change', 'What Would Change Your Mind'),
    ]

    main_question = models.ForeignKey(MainQuestion, on_delete=models.CASCADE, related_name='checkpoints')
    checkpoint_number = models.PositiveIntegerField()  # 1, 2, or 3
    checkpoint_type = models.CharField(max_length=20, choices=CHECKPOINT_TYPES)
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=300, blank=True)
    instruction = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['main_question', 'checkpoint_number']

    def __str__(self):
        return f"{self.main_question.key} - Checkpoint {self.checkpoint_number}"


class Choice(models.Model):
    """A selectable choice within a checkpoint."""
    checkpoint = models.ForeignKey(Checkpoint, on_delete=models.CASCADE, related_name='choices')
    key = models.CharField(max_length=30)  # q10a_cp1_choice1
    title = models.CharField(max_length=500)
    subtitle = models.CharField(max_length=500, blank=True)
    image = models.URLField(blank=True)
    description = models.TextField(blank=True)

    # Extended content fields (varies by checkpoint type)
    # Checkpoint 1 fields
    why_this_matters = models.TextField(blank=True)
    research_evidence = models.TextField(blank=True)
    decision_impact = models.TextField(blank=True)

    # Checkpoint 2 fields
    what_you_are_fighting_for = models.TextField(blank=True)
    cooperative_learning = models.TextField(blank=True)
    barriers_to_access = models.TextField(blank=True)

    # Checkpoint 3 fields
    care_team_affirmation = models.TextField(blank=True)
    interdependency_at_work = models.TextField(blank=True)
    reflection_guidance = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ['checkpoint', 'key']

    def __str__(self):
        return f"{self.checkpoint} - {self.title[:30]}"


# =============================================================================
# USER RESPONSES & EXPLANATIONS
# =============================================================================

class QuestionResponse(models.Model):
    """User's response to a main question (aggregates all 3 checkpoint responses)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_responses')
    main_question = models.ForeignKey(MainQuestion, on_delete=models.CASCADE, related_name='responses')
    is_complete = models.BooleanField(default=False)  # All 3 checkpoints answered
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'main_question']

    def __str__(self):
        return f"{self.user.email} - {self.main_question.key}"


class CheckpointResponse(models.Model):
    """User's selected choices for a specific checkpoint."""
    question_response = models.ForeignKey(QuestionResponse, on_delete=models.CASCADE, related_name='checkpoint_responses')
    checkpoint = models.ForeignKey(Checkpoint, on_delete=models.CASCADE, related_name='responses')
    selected_choices = models.ManyToManyField(Choice, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['checkpoint__order']
        unique_together = ['question_response', 'checkpoint']

    def __str__(self):
        return f"{self.question_response.user.email} - {self.checkpoint}"


class Explanation(models.Model):
    """
    User's explanation after completing a main question.
    Can be video, audio, or text.
    """
    EXPLANATION_TYPES = [
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('text', 'Text'),
    ]

    VISIBILITY_CHOICES = [
        ('private', 'Only Me'),
        ('care_team', 'Care Team'),
        ('public', 'Public'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='explanations')
    question_response = models.ForeignKey(QuestionResponse, on_delete=models.CASCADE, related_name='explanations')

    explanation_type = models.CharField(max_length=10, choices=EXPLANATION_TYPES)

    # Content fields (use appropriate one based on type)
    text_content = models.TextField(blank=True)
    media_file = CloudinaryField('media', blank=True, null=True, resource_type='auto')  # video/audio
    media_url = models.URLField(blank=True)  # Cloudinary URL after upload
    thumbnail_url = models.URLField(blank=True)  # For videos
    duration_seconds = models.PositiveIntegerField(null=True, blank=True)  # For video/audio
    description = models.CharField(max_length=150, blank=True)  # Short description from user

    # Visibility
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='care_team')

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.explanation_type} for {self.question_response.main_question.key}"


# =============================================================================
# CARE TEAM
# =============================================================================

class CareTeam(models.Model):
    """A user's care team group."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owned_care_team')
    name = models.CharField(max_length=200, default="My Care Team")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner.email}'s Care Team"


class TeamMembership(models.Model):
    """Membership in a care team."""
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    ]

    care_team = models.ForeignKey(CareTeam, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    has_affirmed = models.BooleanField(default=False)  # Affirmed the care plan
    affirmed_at = models.DateTimeField(null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['care_team', 'user']

    def __str__(self):
        return f"{self.user.email} in {self.care_team}"


class TeamInvitation(models.Model):
    """Email invitation to join a care team."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('expired', 'Expired'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    care_team = models.ForeignKey(CareTeam, on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    email = models.EmailField()  # Email of invited person
    invited_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_invitations')

    token = models.CharField(max_length=100, unique=True)  # For email link
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)  # Personal message with invitation

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Invitation to {self.email} for {self.care_team}"


# =============================================================================
# SOCIAL INTERACTIONS
# =============================================================================

class Reaction(models.Model):
    """Reactions/likes on explanations."""
    REACTION_TYPES = [
        ('like', '👍'),
        ('love', '❤️'),
        ('support', '🤗'),
        ('insightful', '💡'),
        ('grateful', '🙏'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    explanation = models.ForeignKey(Explanation, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=20, choices=REACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'explanation']  # One reaction per user per explanation

    def __str__(self):
        return f"{self.user.email} - {self.reaction_type} on {self.explanation.id}"


class Comment(models.Model):
    """Comments on explanations."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    explanation = models.ForeignKey(Explanation, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.email} comment on {self.explanation.id}"


# =============================================================================
# AI INTERACTIONS
# =============================================================================

class AIInteraction(models.Model):
    """AI-generated content for explanations (summarize, compare, etc.)."""
    INTERACTION_TYPES = [
        ('summarize', 'Summarize'),
        ('compare', 'Compare'),
        ('clarify', 'Clarify'),
        ('suggest', 'Suggest Questions'),
        ('themes', 'Extract Themes'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_interactions')
    explanation = models.ForeignKey(Explanation, on_delete=models.CASCADE, related_name='ai_interactions', null=True, blank=True)

    # For comparing multiple explanations
    compared_explanations = models.ManyToManyField(Explanation, blank=True, related_name='compared_in')

    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    prompt = models.TextField()  # User's prompt/question
    response = models.TextField()  # AI response

    # Metadata
    model_used = models.CharField(max_length=50, default='gpt-4')  # or claude, etc.
    tokens_used = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.interaction_type} by {self.user.email}"


# =============================================================================
# LEGACY SUPPORT (for existing frontend compatibility)
# =============================================================================

class LegacyTeamMember(models.Model):
    """
    Legacy team member model for backward compatibility.
    TODO: Migrate to CareTeam/TeamMembership system.
    """
    name = models.CharField(max_length=200)
    avatar = models.URLField(blank=True)
    affirmed = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        db_table = 'questionnaire_teammember'  # Keep old table name

    def __str__(self):
        return self.name
