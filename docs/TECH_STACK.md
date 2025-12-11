# AWFM Tech Stack Comparison & Decisions

## Overview

This document outlines the technology choices for AWFM, comparing alternatives and explaining why each was selected.

---

## Proposed Tech Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AWFM TECH STACK                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  FRONTEND          │  BACKEND           │  DATABASE        │  SERVICES      │
│  ─────────────────────────────────────────────────────────────────────────  │
│                    │                    │                  │                │
│  React 18          │  Django 5.x        │  PostgreSQL      │  Cloudinary    │
│  React Router 6    │  DRF 3.14          │                  │  OpenAI API    │
│  Axios             │  Django Channels   │  Redis           │  SendGrid      │
│  React Query       │  Celery            │                  │                │
│                    │                    │                  │                │
│  HOSTING           │  HOSTING           │  HOSTING         │                │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Netlify           │  Railway           │  Railway         │                │
│                    │                    │  Upstash (Redis) │                │
│                    │                    │                  │                │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Backend Framework Comparison

### Django vs Alternatives

| Factor | Django | Node.js/Express | FastAPI | Ruby on Rails |
|--------|--------|-----------------|---------|---------------|
| **Learning Curve** | Moderate | Easy | Easy | Moderate |
| **Development Speed** | Fast | Moderate | Fast | Fast |
| **Batteries Included** | ✅ Everything | ❌ Assemble yourself | ⚠️ Some | ✅ Everything |
| **Admin Panel** | ✅ Built-in | ❌ Build yourself | ❌ Build yourself | ✅ Built-in |
| **ORM** | ✅ Excellent | ⚠️ Various options | ⚠️ SQLAlchemy | ✅ Active Record |
| **Auth System** | ✅ Built-in | ❌ Passport.js | ❌ DIY | ✅ Devise |
| **REST API** | ✅ DRF (excellent) | ✅ Easy | ✅ Native | ⚠️ Jbuilder |
| **Async Support** | ⚠️ Newer | ✅ Native | ✅ Native | ❌ Limited |
| **AI/ML Integration** | ✅ Python ecosystem | ⚠️ Limited | ✅ Python ecosystem | ⚠️ Limited |
| **Community** | Huge | Massive | Growing | Large |
| **Maturity** | 18+ years | 14+ years | 5+ years | 19+ years |

### Why Django for AWFM

```
✅ Batteries Included
   - Admin panel for content management (questions, choices)
   - Built-in auth system (users, permissions)
   - ORM for complex relational queries
   - Forms and validation

✅ Python Ecosystem
   - Easy OpenAI/LangChain integration for ASK AI feature
   - Rich libraries for data processing
   - Celery for background tasks

✅ Django REST Framework
   - Industry standard for APIs
   - Serializers, viewsets, permissions
   - Excellent documentation

✅ Stability & Maturity
   - Well-tested, battle-hardened
   - Long-term support
   - Large talent pool

⚠️ Trade-offs Accepted
   - Async is newer (but improving)
   - Monolithic (but manageable for this project)
```

### Django Pros & Cons

#### Pros
| Advantage | Benefit for AWFM |
|-----------|------------------|
| Admin panel | Easy question/choice management |
| ORM | Complex queries for care teams, responses |
| Auth system | User registration, email invites |
| Security | Built-in CSRF, XSS, SQL injection protection |
| DRF | Clean API design |
| Python | AI/ML integration (OpenAI, LangChain) |
| Celery integration | Background email, AI processing |
| Community | Abundant resources, packages |

#### Cons
| Disadvantage | Mitigation |
|--------------|------------|
| Async limitations | Use Channels for WebSockets |
| Monolithic | Acceptable for project size |
| Slower than Go/Rust | Not a bottleneck for this use case |
| Learning curve | Well-documented, team can learn |

---

## Database Comparison

### PostgreSQL vs MongoDB

| Factor | PostgreSQL | MongoDB |
|--------|-----------|---------|
| **Data Model** | Relational (tables, rows) | Document (JSON-like) |
| **Schema** | Strict schema | Flexible schema |
| **Relationships** | ✅ Native (FK, JOINs) | ❌ Manual references |
| **ACID Compliance** | ✅ Full | ⚠️ Eventual consistency |
| **Complex Queries** | ✅ Excellent | ⚠️ Aggregation pipelines |
| **Django Support** | ✅ Native, first-class | ⚠️ djongo (limited) |
| **JSON Support** | ✅ JSONB type | ✅ Native |
| **Full-text Search** | ✅ Built-in | ✅ Built-in |
| **Transactions** | ✅ Full support | ⚠️ Limited |
| **Maturity** | 30+ years | 15+ years |

### Why PostgreSQL for AWFM

```
AWFM DATA IS INHERENTLY RELATIONAL:

User ──────┬──► QuestionResponse ──► CheckpointResponse ──► Choice
           │
           ├──► CareTeam ──► TeamMembership ──► User
           │
           └──► Explanation ──► Reaction
                           └──► AIInteraction

These relationships require:
- Foreign keys for data integrity
- JOINs for efficient queries
- Transactions for consistency
```

### Real-World Query Examples

```sql
-- PostgreSQL: Get user's care team with all members and their affirmation status
SELECT ct.name, u.email, tm.has_affirmed, tm.affirmed_at
FROM care_teams ct
JOIN team_memberships tm ON ct.id = tm.care_team_id
JOIN users u ON tm.user_id = u.id
WHERE ct.owner_id = '123';

-- MongoDB equivalent: Multiple queries or complex aggregation
db.care_teams.aggregate([
  { $match: { owner_id: '123' } },
  { $lookup: { from: 'team_memberships', ... } },
  { $lookup: { from: 'users', ... } },
  { $unwind: ... }
]);
```

### When to Use MongoDB Instead

MongoDB would be better if:
- Unpredictable schema (not our case)
- Write-heavy with millions of documents
- Storing truly document-centric data (logs, events)
- No complex relationships

**AWFM verdict**: PostgreSQL is clearly better for our relational data model.

---

## Media Storage Comparison

### Cloudinary vs AWS S3

| Factor | Cloudinary | AWS S3 |
|--------|-----------|--------|
| **Setup Time** | 5 minutes | 30+ minutes |
| **Learning Curve** | Very easy | Steeper (IAM, policies) |
| **Video Transcoding** | ✅ Built-in, automatic | ❌ Need MediaConvert (+$) |
| **Audio Processing** | ✅ Built-in | ❌ Need Lambda |
| **Image Optimization** | ✅ On-the-fly | ❌ Need CloudFront/Lambda |
| **CDN** | ✅ Included | ❌ CloudFront extra |
| **Thumbnails** | ✅ Automatic | ❌ Manual |
| **Django Integration** | ✅ Simple package | ⚠️ More config |
| **Pricing Model** | Flat monthly | Pay-per-use |

### Pricing Comparison

#### Cloudinary
| Tier | Storage | Bandwidth | Transformations | Price |
|------|---------|-----------|-----------------|-------|
| Free | 25 GB | 25 GB/mo | 25,000 | $0 |
| Plus | 225 GB | 225 GB/mo | 225,000 | $89/mo |
| Advanced | Custom | Custom | Custom | Custom |

#### AWS S3 + Services
| Service | Cost |
|---------|------|
| S3 Storage | $0.023/GB/mo |
| S3 Bandwidth | $0.09/GB |
| CloudFront CDN | $0.085/GB |
| MediaConvert | $0.015-0.030/min |
| Lambda | $0.20/million requests |

#### Cost Example (100 users, moderate usage)

| Scenario | Cloudinary | AWS S3 + extras |
|----------|-----------|-----------------|
| 50 GB storage | Free | ~$1.15/mo |
| 100 GB bandwidth | $89/mo (Plus) | ~$9/mo |
| Video transcoding | Included | ~$15-30/mo |
| CDN | Included | ~$8.50/mo |
| **Total** | **$0 - $89** | **~$35-50/mo** |

**But AWS requires:**
- More development time
- DevOps expertise
- Multiple services to configure
- Ongoing maintenance

### Why Cloudinary for AWFM

```
AWFM NEEDS:
✅ Video uploads for explanations  → Cloudinary auto-transcodes
✅ Audio uploads                   → Cloudinary handles it
✅ Thumbnails for videos           → Auto-generated
✅ Fast delivery                   → CDN included
✅ Simple Django setup             → 10 lines of config
✅ Focus on features, not infra    → Less complexity

DECISION: Cloudinary
- Faster to implement
- All-in-one solution
- Predictable pricing
- Can migrate to S3 later if needed at scale
```

---

## AI Integration Comparison

### OpenAI vs Claude vs Self-Hosted

| Factor | OpenAI (GPT-4) | Claude | Self-Hosted |
|--------|---------------|--------|-------------|
| **Quality** | ✅ Excellent | ✅ Excellent | ⚠️ Varies |
| **Setup** | Easy (API key) | Easy (API key) | Complex |
| **Cost** | Pay-per-token | Pay-per-token | Infrastructure |
| **Privacy** | Data sent to API | Data sent to API | Full control |
| **Latency** | Low | Low | Depends |
| **Python SDK** | ✅ Excellent | ✅ Good | Varies |

### Why OpenAI for AWFM

```
ASK AI FEATURES:
- Summarize explanations
- Compare team members' views
- Clarify medical concepts
- Extract themes

OPENAI ADVANTAGES:
✅ Best-in-class for summarization
✅ Excellent Python SDK
✅ Easy integration with Django
✅ Predictable API
✅ Large context windows (GPT-4 Turbo: 128k tokens)
```

### Cost Estimate

| Model | Input | Output | Est. Monthly (1000 users) |
|-------|-------|--------|---------------------------|
| GPT-4 Turbo | $0.01/1K tokens | $0.03/1K tokens | ~$50-100 |
| GPT-3.5 Turbo | $0.0005/1K tokens | $0.0015/1K tokens | ~$5-10 |

---

## Deployment Platform Comparison

### Backend: Railway vs Alternatives

| Factor | Railway | Heroku | Render | AWS/GCP |
|--------|---------|--------|--------|---------|
| **Setup** | 5 min | 10 min | 10 min | 1+ hour |
| **Django Support** | ✅ Native | ✅ Native | ✅ Native | ⚠️ Manual |
| **PostgreSQL** | ✅ Included | ✅ Included | ✅ Included | ⚠️ RDS |
| **Auto-deploy** | ✅ GitHub | ✅ GitHub | ✅ GitHub | ⚠️ CodePipeline |
| **SSL** | ✅ Free | ✅ Free | ✅ Free | ⚠️ ACM |
| **Pricing** | $5/mo start | $7/mo start | $7/mo start | Variable |
| **DX** | ✅ Excellent | ✅ Good | ✅ Good | ⚠️ Complex |

### Can Railway Host Both Frontend & Backend?

**Yes**, but here's why we recommend splitting:

| Factor | Railway (Both) | Railway + Netlify |
|--------|---------------|-------------------|
| **Setup** | Simpler (one platform) | Two platforms |
| **Cost** | ~$10-15/mo total | ~$5-10/mo (Netlify free) |
| **Frontend CDN** | ❌ No global CDN | ✅ Global CDN (faster) |
| **Static Hosting** | Overkill (uses compute) | ✅ Optimized for static |
| **Build Times** | Uses Railway minutes | Free on Netlify |
| **Preview Deploys** | ❌ Manual | ✅ Automatic per PR |

**Recommendation:** Use Railway for backend + Netlify for frontend (industry standard, cost-effective)

**Alternative:** Railway-only works fine for MVP if you prefer simplicity

### Frontend: Netlify vs Alternatives

| Factor | Netlify | Vercel | AWS Amplify | GitHub Pages |
|--------|---------|--------|-------------|--------------|
| **Setup** | 2 min | 2 min | 5 min | 5 min |
| **React Support** | ✅ Native | ✅ Native | ✅ Native | ⚠️ Manual |
| **CDN** | ✅ Global | ✅ Global | ✅ Global | ⚠️ Limited |
| **SSL** | ✅ Free | ✅ Free | ✅ Free | ✅ Free |
| **Forms** | ✅ Included | ❌ No | ❌ No | ❌ No |
| **Functions** | ✅ Included | ✅ Included | ✅ Included | ❌ No |
| **Free Tier** | ✅ Generous | ✅ Generous | ⚠️ Limited | ✅ Free |

---

## Final Tech Stack Decision

### Selected Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AWFM PRODUCTION STACK                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  LAYER              TECHNOLOGY           REASON                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  Frontend           React 18             Industry standard, team knows it    │
│  Routing            React Router 6       De facto React routing              │
│  State              React Query          Server state management             │
│  HTTP Client        Axios                Interceptors, error handling        │
│  Frontend Host      Netlify              Free tier, easy deploy              │
│                                                                              │
│  Backend            Django 5.x           Batteries included, Python AI       │
│  API                DRF 3.14             Best REST framework for Django      │
│  Real-time          Django Channels      WebSockets for notifications        │
│  Background         Celery + Redis       Async tasks (email, AI)             │
│  Backend Host       Railway              Easy PostgreSQL, auto-deploy        │
│                                                                              │
│  Database           PostgreSQL           Relational data, Django native      │
│  Cache/Queue        Redis (Upstash)      Sessions, Celery broker             │
│                                                                              │
│  Media Storage      Cloudinary           Video/audio with CDN included       │
│  AI                 OpenAI GPT-4         Summarize, compare explanations     │
│  Email              SendGrid             Transactional emails (invites)      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Why This Stack Works

| Requirement | Solution |
|-------------|----------|
| 30 questions with 3 checkpoints each | PostgreSQL relational model |
| Video/audio explanations | Cloudinary (auto-transcode, CDN) |
| Care team collaboration | Django auth + custom team models |
| Email invitations | SendGrid via django-anymail |
| Real-time reactions | Django Channels + WebSockets |
| ASK AI integration | OpenAI API + Celery background |
| Fast development | Django batteries + DRF |
| Easy deployment | Railway + Netlify |
| Cost-effective | Free tiers cover MVP |

---

## Package List

### Backend (requirements.txt)

```txt
# Django core
Django>=5.0,<6.0
djangorestframework>=3.14,<4.0
django-cors-headers>=4.3,<5.0

# Database
dj-database-url>=2.1,<3.0
psycopg2-binary>=2.9,<3.0

# Media storage
cloudinary>=1.36,<2.0
django-cloudinary-storage>=0.3,<1.0

# Authentication
djangorestframework-simplejwt>=5.3,<6.0

# Background tasks
celery>=5.3,<6.0
redis>=5.0,<6.0

# Email
django-anymail>=10.0,<11.0

# AI integration
openai>=1.0,<2.0

# Server
python-dotenv>=1.0,<2.0
gunicorn>=21.0,<23.0
whitenoise>=6.6,<7.0
```

### Frontend (package.json)

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.2",
    "@tanstack/react-query": "^5.0.0",
    "lottie-react": "^2.4.0"
  }
}
```

---

## Cost Estimate (MVP)

| Service | Free Tier | Paid Estimate |
|---------|-----------|---------------|
| Netlify (Frontend) | 100 GB bandwidth | $0 |
| Railway (Backend) | $5 credit/mo | ~$5-10/mo |
| Railway (PostgreSQL) | Included | Included |
| Upstash (Redis) | 10K commands/day | $0 |
| Cloudinary | 25 GB | $0-89/mo |
| SendGrid | 100 emails/day | $0 |
| OpenAI | Pay-per-use | ~$10-50/mo |
| **TOTAL** | | **$15-150/mo** |

---

## Migration Path

If the app grows significantly:

```
SCALE UP PATH:
─────────────────────────────────────────────────────────────────

Current (MVP)              Scale (1000+ users)        Enterprise
─────────────              ───────────────────        ──────────

Netlify Free        →      Netlify Pro           →   AWS CloudFront
Railway Starter     →      Railway Pro           →   AWS ECS/EKS
Railway Postgres    →      Railway Pro           →   AWS RDS
Upstash Free        →      Upstash Pro           →   AWS ElastiCache
Cloudinary Free     →      Cloudinary Plus       →   AWS S3 + MediaConvert
```

The current stack allows easy migration without major rewrites.
