"""Management command to seed initial questionnaire data for Section 3."""
from django.core.management.base import BaseCommand
from questionnaire.models import (
    Section, MainQuestion, Checkpoint, Choice, LegacyTeamMember
)


class Command(BaseCommand):
    help = 'Seeds the database with Section 3: Advance Care Planning (Part 1) data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with Section 3 data...')

        # =================================================================
        # SECTION 3: ADVANCE CARE PLANNING (PART 1)
        # =================================================================
        section_3, created = Section.objects.update_or_create(
            key='section_3',
            defaults={
                'title': 'ADVANCE CARE PLANNING (PART 1)',
                'description': 'Questions about your preferences for medical interventions and quality of life considerations.',
                'order': 3
            }
        )
        self.stdout.write(f'  {"Created" if created else "Updated"} section: {section_3.title}')

        # =================================================================
        # MAIN QUESTIONS FOR SECTION 3
        # =================================================================
        questions_data = [
            {
                'key': 'q10a',
                'title': 'How important is staying alive even if you have substantial physical limitations?',
                'subtitle': 'Question 10 A',
                'order': 1
            },
            {
                'key': 'q10b',
                'title': 'How important is staying alive even if you have substantial mental limitations?',
                'subtitle': 'Question 10 B',
                'order': 2
            },
            {
                'key': 'q11',
                'title': 'How important is physical comfort or being pain-free for you?',
                'subtitle': 'Question 11',
                'order': 3
            },
            {
                'key': 'q12',
                'title': 'How important is being independent for you?',
                'subtitle': 'Question 12',
                'order': 4
            },
            {
                'key': 'q13',
                'title': 'Do you want life support to keep you alive no matter what?',
                'subtitle': 'Question 13',
                'order': 5
            },
            {
                'key': 'q14',
                'title': 'Do you want a feeding tube if you can\'t swallow food or drink water?',
                'subtitle': 'Question 14',
                'order': 6
            },
            {
                'key': 'q15',
                'title': 'Do you want pain medicine even if it speeds dying?',
                'subtitle': 'Question 15',
                'order': 7
            },
        ]

        main_questions = {}
        for q_data in questions_data:
            question, created = MainQuestion.objects.update_or_create(
                key=q_data['key'],
                defaults={
                    'section': section_3,
                    'title': q_data['title'],
                    'subtitle': q_data['subtitle'],
                    'order': q_data['order']
                }
            )
            main_questions[q_data['key']] = question
            self.stdout.write(f'  {"Created" if created else "Updated"} question: {question.key}')

        # =================================================================
        # CHECKPOINTS FOR EACH QUESTION (3 per question)
        # =================================================================
        checkpoint_templates = [
            {
                'checkpoint_number': 1,
                'checkpoint_type': 'position',
                'title': 'What concerns, issues, and challenges might you be facing?',
                'subtitle': 'Checkpoint 1: Your Position',
                'instruction': 'Select the option that best represents what matters most to you.'
            },
            {
                'checkpoint_number': 2,
                'checkpoint_type': 'challenges',
                'title': 'What challenges might change your position?',
                'subtitle': 'Checkpoint 2: Your Challenges',
                'instruction': 'Select all that apply to your situation.'
            },
            {
                'checkpoint_number': 3,
                'checkpoint_type': 'change',
                'title': 'What would make you change your mind?',
                'subtitle': 'Checkpoint 3: What Would Change Your Mind',
                'instruction': 'Select all circumstances that might change your decision.'
            }
        ]

        checkpoints = {}
        for q_key, main_question in main_questions.items():
            checkpoints[q_key] = {}
            for cp_data in checkpoint_templates:
                checkpoint, created = Checkpoint.objects.update_or_create(
                    main_question=main_question,
                    checkpoint_number=cp_data['checkpoint_number'],
                    defaults={
                        'checkpoint_type': cp_data['checkpoint_type'],
                        'title': cp_data['title'],
                        'subtitle': cp_data['subtitle'],
                        'instruction': cp_data['instruction'],
                        'order': cp_data['checkpoint_number']
                    }
                )
                checkpoints[q_key][cp_data['checkpoint_number']] = checkpoint
                self.stdout.write(f'    {"Created" if created else "Updated"} checkpoint: {checkpoint}')

        # =================================================================
        # CHOICES FOR Q10A (example - full implementation)
        # =================================================================
        self._seed_q10a_choices(checkpoints['q10a'])

        # =================================================================
        # LEGACY TEAM MEMBERS (for backward compatibility)
        # =================================================================
        team_data = [
            {'name': 'Dr. Sarah', 'avatar': 'https://i.pravatar.cc/82?img=1', 'affirmed': True, 'order': 1},
            {'name': 'John', 'avatar': 'https://i.pravatar.cc/82?img=2', 'affirmed': True, 'order': 2},
            {'name': 'Mary', 'avatar': 'https://i.pravatar.cc/82?img=3', 'affirmed': False, 'order': 3},
            {'name': 'James', 'avatar': 'https://i.pravatar.cc/82?img=4', 'affirmed': False, 'order': 4},
            {'name': 'Lisa', 'avatar': 'https://i.pravatar.cc/82?img=5', 'affirmed': False, 'order': 5},
        ]

        for t in team_data:
            member, created = LegacyTeamMember.objects.update_or_create(
                name=t['name'],
                defaults={
                    'avatar': t['avatar'],
                    'affirmed': t['affirmed'],
                    'order': t['order']
                }
            )
            self.stdout.write(f'  {"Created" if created else "Updated"} team member: {member.name}')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def _seed_q10a_choices(self, checkpoints):
        """Seed choices for Q10A - Physical limitations question."""

        # Checkpoint 1 Choices
        cp1_choices = [
            {
                'key': 'q10a_cp1_1',
                'title': 'Life extension is very important regardless of function',
                'subtitle': 'Life extension is very important regardless of function',
                'image': 'https://images.unsplash.com/photo-1559757175-5700dde675bc?w=600&h=400&fit=crop',
                'description': "Life is sacred to me - every moment matters regardless of what I can or can't do. Modern medicine works miracles I can't predict. Keep fighting for me with every tool available.",
                'why_this_matters': "Shapes all treatment escalation decisions - ICU admission, ventilation, dialysis, CPR. 82.4% physicians underestimate disability quality of life.",
                'research_evidence': "Albrecht & Devlieger 1999: 54.3% with moderate-serious disabilities report excellent/good QOL. ICU surrogate research: 33-35% PTSD at 6 months.",
                'decision_impact': "You'll receive maximum intervention including ventilators, dialysis, feeding tubes, CPR regardless of prognosis.",
                'order': 1
            },
            {
                'key': 'q10a_cp1_2',
                'title': 'Staying alive somewhat important, depends on situation',
                'subtitle': 'Staying alive somewhat important, depends on situation',
                'image': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=600&h=400&fit=crop',
                'description': "I value being alive, but not at any cost. It depends on whether I can still connect with people I love, experience some joy, maintain dignity.",
                'why_this_matters': "Preferences shift based on actual vs imagined experience. 70.3% lack capacity when decisions needed, forcing surrogates to guess intent.",
                'research_evidence': "Preference stability: 35-49% show inconsistent preference trajectories. Surrogate accuracy: predict wishes correctly 68% of time.",
                'decision_impact': "You'll receive selective interventions based on perceived potential for meaningful recovery.",
                'order': 2
            },
            {
                'key': 'q10a_cp1_3',
                'title': 'Avoid aggressive intervention if function seriously declined',
                'subtitle': 'Avoid aggressive intervention if function seriously declined',
                'image': 'https://images.unsplash.com/photo-1518495973542-4542c06a5843?w=600&h=400&fit=crop',
                'description': "My biggest fear isn't death—it's existing without really living. If I've lost capacity for meaningful experience, focus on comfort.",
                'why_this_matters': "'Seriously declined' interpreted differently by family vs medical team, creating conflict. 82.4% physicians underestimate disability QOL.",
                'research_evidence': "Quality of life highly subjective. Disability paradox: people adapt to limitations better than predicted.",
                'decision_impact': "You'll avoid interventions prolonging dying process—no CPR, ventilators, dialysis when function severely declined.",
                'order': 3
            }
        ]

        for choice_data in cp1_choices:
            choice, created = Choice.objects.update_or_create(
                checkpoint=checkpoints[1],
                key=choice_data['key'],
                defaults={
                    'title': choice_data['title'],
                    'subtitle': choice_data['subtitle'],
                    'image': choice_data['image'],
                    'description': choice_data['description'],
                    'why_this_matters': choice_data['why_this_matters'],
                    'research_evidence': choice_data['research_evidence'],
                    'decision_impact': choice_data['decision_impact'],
                    'order': choice_data['order']
                }
            )
            self.stdout.write(f'      {"Created" if created else "Updated"} choice: {choice.key}')

        # Checkpoint 2 Choices
        cp2_choices = [
            {
                'key': 'q10a_cp2_1',
                'title': 'Worried doctors might undervalue my life with disability',
                'subtitle': 'Worried doctors might undervalue my life with disability',
                'image': 'https://images.unsplash.com/photo-1584515933487-779824d29309?w=600&h=400&fit=crop',
                'description': "What terrifies me is providers deciding my disabled life isn't worth saving. My quality of life is mine to assess.",
                'what_you_are_fighting_for': "Having a say (maintaining autonomy against bias), Sense of peace (knowing directive will be honored).",
                'cooperative_learning': "Provider bias disrupts all 5 elements: team must maintain shared vision against medical pressure.",
                'barriers_to_access': "Multiply marginalized disabled people face compounded bias: Black disabled encounter both racism and ableism.",
                'order': 1
            },
            {
                'key': 'q10a_cp2_2',
                'title': 'Uncertain what life with physical limitations is like',
                'subtitle': 'Uncertain what life with physical limitations is like',
                'image': 'https://images.unsplash.com/photo-1493836512294-502baa1986e2?w=600&h=400&fit=crop',
                'description': "I have no idea what life with severe disability would actually be like. My assumptions are probably shaped by societal fear.",
                'what_you_are_fighting_for': "Honesty about uncertainty (acknowledges knowledge limits).",
                'cooperative_learning': "Uncertainty strains all 5 elements: Positive interdependence requires shared understanding of values.",
                'barriers_to_access': "Able-bodied imagination of disability shaped by societal segregation. Disabled people rarely in media.",
                'order': 2
            },
            {
                'key': 'q10a_cp2_3',
                'title': 'Worried about becoming a burden to loved ones',
                'subtitle': 'Worried about becoming a burden to loved ones',
                'image': 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=600&h=400&fit=crop',
                'description': "The guilt of what caring for me would do to my family weighs heavily. I'd rather go sooner than watch them sacrifice everything.",
                'what_you_are_fighting_for': "Not burdening loved ones (primary motivation).",
                'cooperative_learning': "Burden fear affects all 5 elements: belief you're burden undermines shared commitment.",
                'barriers_to_access': "Marginalized groups face disproportionate burden fear: Women socialized to self-sacrifice.",
                'order': 3
            },
            {
                'key': 'q10a_cp2_4',
                'title': 'Have seen others struggle with physical limitations',
                'subtitle': 'Have seen others struggle with physical limitations',
                'image': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=600&h=400&fit=crop',
                'description': "I watched someone I love struggle with severe limitations. That witnessing drives my decisions more than any abstract thinking.",
                'what_you_are_fighting_for': "Avoiding prolonged dying (witnessed suffering), Having a say (informed by observation).",
                'cooperative_learning': "Witnessed trauma affects all 5 elements: shared trauma may create unified fear or divided interpretations.",
                'barriers_to_access': "Whose struggle gets witnessed and interpreted how? Middle-class families can hire help, reducing visible struggle.",
                'order': 4
            }
        ]

        for choice_data in cp2_choices:
            choice, created = Choice.objects.update_or_create(
                checkpoint=checkpoints[2],
                key=choice_data['key'],
                defaults={
                    'title': choice_data['title'],
                    'subtitle': choice_data['subtitle'],
                    'image': choice_data['image'],
                    'description': choice_data['description'],
                    'what_you_are_fighting_for': choice_data['what_you_are_fighting_for'],
                    'cooperative_learning': choice_data['cooperative_learning'],
                    'barriers_to_access': choice_data['barriers_to_access'],
                    'order': choice_data['order']
                }
            )
            self.stdout.write(f'      {"Created" if created else "Updated"} choice: {choice.key}')

        # Checkpoint 3 Choices
        cp3_choices = [
            {
                'key': 'q10a_cp3_1',
                'title': 'Meeting people with disabilities living meaningful lives',
                'subtitle': 'Meeting people with disabilities living meaningful lives',
                'image': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=400&fit=crop',
                'description': "If 54.3% with serious disabilities report good quality of life, maybe my assumptions are the problem.",
                'care_team_affirmation': "We commit to connecting you with disabled communities, facilitating conversations with people living adapted lives.",
                'interdependency_at_work': "Paradigm shift demands extensive unlearning: Examining internalized ableism accumulated over lifetime.",
                'reflection_guidance': "What specific disabilities terrify you most? Where did these fears originate?",
                'order': 1
            },
            {
                'key': 'q10a_cp3_2',
                'title': "Having my team's support to coordinate medical advocacy",
                'subtitle': "Having my team's support to coordinate medical advocacy",
                'image': 'https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=600&h=400&fit=crop',
                'description': "If I knew my people could work together to fight for what I want, I might choose differently.",
                'care_team_affirmation': "We commit to structured advocacy: defined roles, shift scheduling, communication systems.",
                'interdependency_at_work': "Advocacy coordination demands extraordinary infrastructure: Communication systems for 24/7 updates.",
                'reflection_guidance': "Who specifically would advocate—names, not roles? Can they commit 15-20 hours weekly each?",
                'order': 2
            },
            {
                'key': 'q10a_cp3_3',
                'title': 'Learning more about medical interventions and their outcomes',
                'subtitle': 'Learning more about medical interventions and their outcomes',
                'image': 'https://images.unsplash.com/photo-1511895426328-dc8714191300?w=600&h=400&fit=crop',
                'description': "Maybe if I truly understood what 'mechanical ventilation' means—not just the tube, but the sedation, the weaning process.",
                'care_team_affirmation': "We commit to comprehensive education: not just statistics but what the survivors experience afterward.",
                'interdependency_at_work': "Comprehensive education demands significant resources: Time for multiple consultations.",
                'reflection_guidance': "What specific interventions do you need explained—CPR, ventilation, dialysis, feeding tubes?",
                'order': 3
            },
            {
                'key': 'q10a_cp3_4',
                'title': "Understanding disability doesn't mean low quality of life",
                'subtitle': "Understanding disability doesn't mean low quality of life",
                'image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop',
                'description': "Research says people adapt remarkably, find joy despite limitations I'd assume unbearable.",
                'care_team_affirmation': "We commit to unlearning alongside you: exploring disability paradox research, centering disabled voices.",
                'interdependency_at_work': "Paradigm shift demands extensive unlearning: Examining internalized ableism.",
                'reflection_guidance': "Have you known thriving disabled people or only suffering narratives?",
                'order': 4
            }
        ]

        for choice_data in cp3_choices:
            choice, created = Choice.objects.update_or_create(
                checkpoint=checkpoints[3],
                key=choice_data['key'],
                defaults={
                    'title': choice_data['title'],
                    'subtitle': choice_data['subtitle'],
                    'image': choice_data['image'],
                    'description': choice_data['description'],
                    'care_team_affirmation': choice_data['care_team_affirmation'],
                    'interdependency_at_work': choice_data['interdependency_at_work'],
                    'reflection_guidance': choice_data['reflection_guidance'],
                    'order': choice_data['order']
                }
            )
            self.stdout.write(f'      {"Created" if created else "Updated"} choice: {choice.key}')
