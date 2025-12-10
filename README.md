# AWFM Questionnaire - Django Backend

## Quick Start

### 1. Set up virtual environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Run migrations & seed data

```bash
python manage.py migrate
python manage.py seed_data
```

### 5. Create admin user (optional)

```bash
python manage.py createsuperuser
```

### 6. Run development server

```bash
python manage.py runserver
```

- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/main-question/` | GET | Get main screen question |
| `/api/questions/` | GET | Get question metadata (q1, q2, q3) |
| `/api/choices/q1/` | GET | Get Checkpoint 1 choices |
| `/api/choices/q2/` | GET | Get Checkpoint 2 choices |
| `/api/choices/q3/` | GET | Get Checkpoint 3 choices |
| `/api/team/` | GET | Get team members with affirmation status |
| `/api/responses/` | GET, POST | List/create user responses |
| `/api/health/` | GET | Health check |

## Data Structure

```
MainScreenQuestion (singleton)
├── title: "How important is staying alive..."
├── subtitle: "Question 10 A"
└── sectionLabel: "Advance Care Planning"

Question (q1, q2, q3)
├── title, subtitle, checkpointLabel, instruction
└── choices[]
    ├── id, title, subtitle, image, description
    ├── Q1: whyThisMatters, researchEvidence, decisionImpact
    ├── Q2: whatYouAreFightingFor, cooperativeLearning, barriersToAccess
    └── Q3: careTeamAffirmation, interdependencyAtWork, reflectionGuidance

TeamMember
├── id, name, avatar, affirmed
```

## Deployment (Railway)

1. Create a new Railway project
2. Add PostgreSQL database
3. Set environment variables:
   - `SECRET_KEY` - Generate a secure key
   - `DEBUG` - Set to `False`
   - `ALLOWED_HOSTS` - Your Railway domain
   - `CORS_ALLOWED_ORIGINS` - Your frontend URL
   - `DATABASE_URL` - Auto-set by Railway PostgreSQL

Railway will automatically:
- Detect the Python project
- Use the `Procfile` for startup
- Run migrations and seed data on deploy
