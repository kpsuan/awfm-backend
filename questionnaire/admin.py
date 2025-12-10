"""Admin configuration for the AWFM Questionnaire."""
from django.contrib import admin
from .models import Question, Choice, TeamMember, MainScreenQuestion, Response


@admin.register(MainScreenQuestion)
class MainScreenQuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'section_label']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['key', 'title', 'subtitle', 'checkpoint_label', 'order']
    list_editable = ['order']
    ordering = ['order']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_id', 'question', 'title_short', 'order']
    list_filter = ['question']
    list_editable = ['order']
    search_fields = ['title', 'description']
    ordering = ['question__order', 'order']

    fieldsets = (
        ('Basic Info', {
            'fields': ('question', 'choice_id', 'title', 'subtitle', 'image', 'description', 'order')
        }),
        ('Checkpoint 1 Content', {
            'fields': ('why_this_matters', 'research_evidence', 'decision_impact'),
            'classes': ('collapse',)
        }),
        ('Checkpoint 2 Content', {
            'fields': ('what_you_are_fighting_for', 'cooperative_learning', 'barriers_to_access'),
            'classes': ('collapse',)
        }),
        ('Checkpoint 3 Content', {
            'fields': ('care_team_affirmation', 'interdependency_at_work', 'reflection_guidance'),
            'classes': ('collapse',)
        }),
    )

    def title_short(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_short.short_description = 'Title'


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'affirmed', 'order']
    list_editable = ['affirmed', 'order']


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'question', 'created_at']
    list_filter = ['question', 'created_at']
    search_fields = ['user_id']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['selected_choices']
