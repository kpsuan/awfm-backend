# AWFM Application Architecture

## Overview

AWFM (A Way Forward Matters) is an advance care planning application that helps users document their healthcare preferences through guided questionnaires, explanations, and care team collaboration.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                        │
│                         React + React Router                                 │
│                                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Pages     │  │ Components  │  │  Services   │  │   Context   │        │
│  │             │  │             │  │             │  │             │        │
│  │ - Questions │  │ - Cards     │  │ - api.js    │  │ - Auth      │        │
│  │ - Team      │  │ - Forms     │  │ - question  │  │ - Question  │        │
│  │ - Summary   │  │ - Media     │  │ - team      │  │ - Team      │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                                              │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │ REST API (JSON)
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND                                         │
│                    Django + Django REST Framework                            │
│                                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │    Views    │  │ Serializers │  │   Models    │  │    URLs     │        │
│  │             │  │             │  │             │  │             │        │
│  │ - Question  │  │ - Question  │  │ - User      │  │ /api/...    │        │
│  │ - Response  │  │ - Response  │  │ - Section   │  │             │        │
│  │ - Team      │  │ - Team      │  │ - Question  │  │             │        │
│  │ - AI        │  │ - AI        │  │ - Response  │  │             │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                                              │
└───────┬─────────────────┬─────────────────┬─────────────────┬───────────────┘
        │                 │                 │                 │
        ▼                 ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  PostgreSQL  │  │  Cloudinary  │  │    Redis     │  │   OpenAI     │
│              │  │              │  │              │  │              │
│  - Users     │  │  - Videos    │  │  - Cache     │  │  - Summarize │
│  - Questions │  │  - Audio     │  │  - Sessions  │  │  - Compare   │
│  - Responses │  │  - Images    │  │  - Celery    │  │  - Clarify   │
│  - Teams     │  │              │  │              │  │              │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

---

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           QUESTIONNAIRE STRUCTURE                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│   Section    │ 1───* │   MainQuestion   │ 1───* │  Checkpoint  │
├──────────────┤       ├──────────────────┤       ├──────────────┤
│ key          │       │ key              │       │ number (1-3) │
│ title        │       │ title            │       │ type         │
│ description  │       │ subtitle         │       │ title        │
│ order        │       │ section_id (FK)  │       │ main_q (FK)  │
└──────────────┘       │ order            │       │ instruction  │
                       └──────────────────┘       └──────┬───────┘
                                                         │
                                                         │ 1
                                                         │
                                                         ▼ *
                                                  ┌──────────────┐
                                                  │    Choice    │
                                                  ├──────────────┤
                                                  │ key          │
                                                  │ title        │
                                                  │ description  │
                                                  │ image        │
                                                  │ [extended]   │
                                                  └──────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER & RESPONSES                                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐       ┌────────────────────┐       ┌─────────────────────┐
│     User     │ 1───* │  QuestionResponse  │ 1───* │ CheckpointResponse  │
├──────────────┤       ├────────────────────┤       ├─────────────────────┤
│ id (UUID)    │       │ user_id (FK)       │       │ question_resp (FK)  │
│ email        │       │ main_question (FK) │       │ checkpoint (FK)     │
│ username     │       │ is_complete        │       │ selected_choices    │
│ avatar       │       │ created_at         │       │ (M2M → Choice)      │
└──────┬───────┘       └─────────┬──────────┘       └─────────────────────┘
       │                         │
       │                         │ 1
       │                         ▼ *
       │                  ┌──────────────┐       ┌──────────────┐
       │                  │ Explanation  │ 1───* │   Reaction   │
       │                  ├──────────────┤       ├──────────────┤
       │                  │ type (v/a/t) │       │ user_id (FK) │
       │                  │ media_url    │       │ type (emoji) │
       │                  │ text_content │       └──────────────┘
       │                  │ visibility   │
       │                  └──────┬───────┘
       │                         │ 1
       │                         ▼ *
       │                  ┌──────────────┐
       │                  │AIInteraction │
       │                  ├──────────────┤
       │                  │ type         │
       │                  │ prompt       │
       │                  │ response     │
       │                  │ model_used   │
       │                  └──────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                              CARE TEAM                                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────┐       ┌──────────────────┐       ┌──────────────┐
│     User     │ 1───1 │    CareTeam      │ 1───* │ Membership   │
│   (owner)    │       ├──────────────────┤       ├──────────────┤
└──────────────┘       │ name             │       │ user_id (FK) │
                       │ owner_id (FK)    │       │ role         │
                       │ description      │       │ has_affirmed │
                       └────────┬─────────┘       └──────────────┘
                                │
                                │ 1
                                ▼ *
                       ┌──────────────────┐
                       │  TeamInvitation  │
                       ├──────────────────┤
                       │ email            │
                       │ token            │
                       │ status           │
                       │ expires_at       │
                       └──────────────────┘
```

---

## Data Models

### Questionnaire Structure

| Model | Purpose | Key Fields |
|-------|---------|------------|
| `Section` | Groups related questions | key, title, order |
| `MainQuestion` | Individual question (e.g., Q10A) | key, title, section_id |
| `Checkpoint` | Sub-question within main (3 per question) | number, type, main_question_id |
| `Choice` | Selectable answer option | key, title, description, checkpoint_id |

### User & Responses

| Model | Purpose | Key Fields |
|-------|---------|------------|
| `User` | Custom user with UUID | id, email, username, avatar |
| `QuestionResponse` | User's answer to main question | user_id, main_question_id, is_complete |
| `CheckpointResponse` | User's choices per checkpoint | question_response_id, selected_choices (M2M) |
| `Explanation` | Video/audio/text after question | type, media_url, text_content, visibility |

### Social Features

| Model | Purpose | Key Fields |
|-------|---------|------------|
| `Reaction` | Likes/reactions on explanations | user_id, explanation_id, type |
| `Comment` | Comments on explanations | user_id, explanation_id, content |
| `AIInteraction` | AI-generated insights | type, prompt, response, explanation_id |

### Care Team

| Model | Purpose | Key Fields |
|-------|---------|------------|
| `CareTeam` | User's care team group | owner_id, name |
| `TeamMembership` | Member of a care team | care_team_id, user_id, role, has_affirmed |
| `TeamInvitation` | Email invitation to join | email, token, status, expires_at |

---

## Questionnaire Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         USER QUESTIONNAIRE JOURNEY                           │
└─────────────────────────────────────────────────────────────────────────────┘

     SECTION 3: ADVANCE CARE PLANNING (PART 1)
     ─────────────────────────────────────────

     ┌─────────────────────────────────────────────────────────────────┐
     │                         Q10A                                     │
     │   "How important is staying alive with physical limitations?"   │
     └─────────────────────────────────────────────────────────────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          ▼                         ▼                         ▼
    ┌───────────┐            ┌───────────┐            ┌───────────┐
    │Checkpoint │            │Checkpoint │            │Checkpoint │
    │     1     │───────────►│     2     │───────────►│     3     │
    │           │            │           │            │           │
    │  "Your    │            │  "Your    │            │  "What    │
    │ Position" │            │Challenges"│            │  Would    │
    │           │            │           │            │  Change"  │
    │ [3 opts]  │            │ [4 opts]  │            │ [4 opts]  │
    └───────────┘            └───────────┘            └───────────┘
                                                            │
                                                            ▼
                                               ┌─────────────────────┐
                                               │      SUMMARY        │
                                               │   (View choices)    │
                                               └──────────┬──────────┘
                                                          │
                                                          ▼
                                               ┌─────────────────────┐
                                               │  TEAM_VISIBILITY    │
                                               │  "You Did It!"      │
                                               │                     │
                                               │  Choose to record:  │
                                               │  📹 Video           │
                                               │  🎙️ Audio           │
                                               │  📝 Text            │
                                               └──────────┬──────────┘
                                                          │
                                                          ▼
                                               ┌─────────────────────┐
                                               │   RECORD_VIDEO      │
                                               │   RECORD_AUDIO      │
                                               │   RECORD_TEXT       │
                                               │                     │
                                               │  - Record/type      │
                                               │  - Add description  │
                                               │    (150 chars max)  │
                                               │  - Review & submit  │
                                               └──────────┬──────────┘
                                                          │
                                                          ▼
                                               ┌─────────────────────┐
                                               │ RECORDING_COMPLETE  │
                                               │                     │
                                               │ "A Whole Family     │
                                               │  Matter"            │
                                               │                     │
                                               │ [I'm Ready] [Skip]  │
                                               └──────────┬──────────┘
                                                          │
                                    ┌─────────────────────┴────────────────┐
                                    ▼                                      ▼
                          ┌─────────────────────┐                ┌──────────────┐
                          │   TEAM_RECORDINGS   │                │   SUMMARY    │
                          │                     │                │   (Skip)     │
                          │ View care team's    │                └──────────────┘
                          │ explanations for    │
                          │ THIS question       │
                          │                     │
                          │ Features:           │
                          │ - Carousel view     │
                          │ - 👍 Like           │
                          │ - 💬 Comment        │
                          │ - 📤 Share          │
                          │ - 🤖 Ask AI         │
                          │ - ✅ Affirm         │
                          │ - 📄 Full Report    │
                          └──────────┬──────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │   NEXT QUESTION     │
                          │       Q10B          │
                          └─────────────────────┘
```

---

## Care Team Explanations Feature

After completing each question, users can:
1. **Record their explanation** (video, audio, or text)
2. **View their care team's explanations** for the same question
3. **Interact** with team members' recordings

### Team Recordings Features

| Feature | Description |
|---------|-------------|
| **Carousel View** | Swipe through team members' recordings |
| **Multiple Formats** | Support for video, audio, and text |
| **Like** | React to team members' explanations |
| **Comment** | Add comments on recordings |
| **Share** | Share recordings externally |
| **Ask AI** | Get AI insights about recordings |
| **Affirm** | Affirm commitment to team member's care plan |
| **Full Report** | View complete summary of member's choices |

### Recording Data Structure

```javascript
{
  type: 'video' | 'audio' | 'text',
  media_url: 'https://cloudinary.com/...',      // For video/audio
  thumbnail_url: 'https://cloudinary.com/...',  // For video
  text_content: '...',                          // For text
  duration_seconds: 45,                         // For video/audio
  description: 'My thoughts on...',             // 150 chars max
  visibility: 'care_team',
  question_response_id: 123
}
```

---

## API Endpoints

### Questionnaire

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sections/` | List all sections |
| GET | `/api/sections/{key}/` | Get section with questions |
| GET | `/api/questions/` | List all main questions |
| GET | `/api/questions/{key}/` | Get question with checkpoints |
| GET | `/api/checkpoints/{id}/` | Get checkpoint with choices |

### Responses

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/responses/` | List user's responses |
| POST | `/api/responses/` | Create/update response |
| GET | `/api/responses/{id}/` | Get specific response |

### Explanations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/explanations/` | List explanations (filtered by visibility) |
| POST | `/api/explanations/` | Upload explanation |
| POST | `/api/explanations/{id}/reactions/` | Add reaction |
| GET | `/api/explanations/{id}/ai/` | Get AI interactions |
| POST | `/api/explanations/{id}/ai/` | Request AI analysis |

### Care Team

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/care-team/` | Get user's care team |
| POST | `/api/care-team/invite/` | Send invitation |
| POST | `/api/invitations/{token}/accept/` | Accept invitation |
| POST | `/api/care-team/members/{id}/affirm/` | Affirm care plan |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health/` | Health check |

---

## Section Structure (All 5 Sections)

```
SECTION 1: [TBD]
├── Q1 - Q9 (questions TBD)
│
SECTION 2: [TBD]
├── Questions TBD
│
SECTION 3: ADVANCE CARE PLANNING (PART 1)  ← Current Focus
├── Q10A — Physical limitations importance
├── Q10B — Mental limitations importance
├── Q11  — Physical comfort importance
├── Q12  — Independence importance
├── Q13  — Life support preference
├── Q14  — Feeding tube preference
├── Q15  — Pain medicine preference
│
SECTION 4: [TBD]
├── Questions TBD
│
SECTION 5: [TBD]
├── Questions TBD (up to Q30)

TOTAL: 30 Questions × 3 Checkpoints = 90 Checkpoint interactions
       + 30 Explanations (video/audio/text)
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PRODUCTION                                      │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────────┐
                    │      Netlify        │
                    │   (React Frontend)  │
                    │                     │
                    │  - Static hosting   │
                    │  - CDN              │
                    │  - SSL              │
                    └──────────┬──────────┘
                               │
                               │ HTTPS
                               ▼
                    ┌─────────────────────┐
                    │      Railway        │
                    │  (Django Backend)   │
                    │                     │
                    │  - Gunicorn         │
                    │  - Auto-deploy      │
                    │  - SSL              │
                    └──────────┬──────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│    Railway      │  │   Cloudinary    │  │     Redis       │
│   PostgreSQL    │  │                 │  │    (Upstash)    │
│                 │  │  - Videos       │  │                 │
│  - All data     │  │  - Audio        │  │  - Cache        │
│  - Backups      │  │  - Images       │  │  - Sessions     │
│                 │  │  - CDN          │  │  - Celery       │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## Environment Variables

```bash
# Django
SECRET_KEY=<generate-secure-key>
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app

# Database
DATABASE_URL=postgres://user:pass@host:5432/dbname

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend.netlify.app

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud
CLOUDINARY_API_KEY=your-key
CLOUDINARY_API_SECRET=your-secret

# OpenAI (for ASK AI)
OPENAI_API_KEY=sk-your-key

# Redis (optional, for Celery)
REDIS_URL=redis://...

# Email (optional)
SENDGRID_API_KEY=your-key
```

---

## Getting Started

```bash
# 1. Clone and setup
cd awfm-backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your values

# 3. Run migrations
python manage.py makemigrations
python manage.py migrate

# 4. Seed initial data
python manage.py seed_data

# 5. Create admin user
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

---

## Next Steps

1. **Phase 1** - Complete Section 3 (Q10A-Q15) with all checkpoints
2. **Phase 2** - Add explanation recording (Cloudinary integration)
3. **Phase 3** - Implement Care Team features
4. **Phase 4** - Add ASK AI integration
5. **Phase 5** - Add remaining sections (1, 2, 4, 5)
