# Environment & CI/CD Setup

## Overview

AWFM uses a three-environment strategy with automated CI/CD pipelines.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ENVIRONMENT PIPELINE                                  │
└─────────────────────────────────────────────────────────────────────────────┘

  Developer        GitHub Actions         Railway/Netlify        Users
  ─────────        ──────────────         ───────────────        ─────

  ┌─────────┐      ┌─────────────┐       ┌─────────────┐
  │ feature │─────►│   PR Test   │       │             │
  │ branch  │      │   (lint,    │       │             │
  └─────────┘      │   test)     │       │             │
       │           └─────────────┘       │             │
       │                                 │             │
       ▼                                 │             │
  ┌─────────┐      ┌─────────────┐       │             │
  │ develop │─────►│ Test + Deploy├─────►│  STAGING    │───► QA Team
  │ branch  │      │   Staging   │       │             │     Testers
  └─────────┘      └─────────────┘       │             │
       │                                 │             │
       │ (PR + Review)                   │             │
       ▼                                 │             │
  ┌─────────┐      ┌─────────────┐       │             │
  │  main   │─────►│ Test + Deploy├─────►│ PRODUCTION  │───► End Users
  │ branch  │      │  Production │       │             │
  └─────────┘      └─────────────┘       └─────────────┘
```

---

## Environments

### 1. Local Development

```bash
# Backend
cd awfm-backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver  # http://localhost:8000

# Frontend
cd prototype/client
npm install
npm start  # http://localhost:3000
```

**Local Config:**
- SQLite database (default)
- Mock data enabled
- No real emails
- `DEBUG=True`

### 2. Staging Environment

**Purpose:** Testing before production release

**URLs:**
- Frontend: `https://staging--yourapp.netlify.app`
- Backend: `https://api-staging.yourapp.railway.app`

**Deployed from:** `develop` branch

**Config:**
- Separate PostgreSQL database
- Real Cloudinary (staging folder)
- Test email (sandbox mode)
- `DEBUG=True`

### 3. Production Environment

**Purpose:** Live users

**URLs:**
- Frontend: `https://yourapp.com`
- Backend: `https://api.yourapp.railway.app`

**Deployed from:** `main` branch

**Config:**
- Production PostgreSQL database
- Production Cloudinary
- Real email sending
- `DEBUG=False`
- SSL enforced

---

## Branch Strategy

```
main (production)
  │
  └── develop (staging)
        │
        ├── feature/user-auth
        ├── feature/video-recording
        ├── bugfix/login-issue
        └── hotfix/critical-bug (→ main directly)
```

### Workflow

1. **Create feature branch** from `develop`
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/my-feature
   ```

2. **Work on feature**, commit regularly
   ```bash
   git add .
   git commit -m "Add feature X"
   ```

3. **Push and create PR** to `develop`
   ```bash
   git push -u origin feature/my-feature
   # Create PR on GitHub: feature/my-feature → develop
   ```

4. **CI runs tests** on PR

5. **Merge to develop** → Auto-deploys to Staging

6. **Test on Staging**

7. **Create PR** from `develop` → `main`

8. **Merge to main** → Auto-deploys to Production

---

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# Triggered on push/PR to main or develop

jobs:
  test:
    # Runs on ALL pushes and PRs
    - Checkout code
    - Setup Python/Node
    - Install dependencies
    - Run linting
    - Run tests

  deploy-staging:
    # Only on push to develop (after tests pass)
    - Deploy to Railway staging
    - Run migrations

  deploy-production:
    # Only on push to main (after tests pass)
    - Deploy to Railway production
    - Run migrations
```

### Pipeline Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         CI/CD PIPELINE                                    │
└──────────────────────────────────────────────────────────────────────────┘

Push/PR to develop or main
         │
         ▼
┌─────────────────┐
│   LINT & TEST   │──────── Fail ────► ❌ Block merge
│                 │
│  - flake8       │
│  - pytest       │
│  - npm test     │
└────────┬────────┘
         │ Pass
         ▼
┌─────────────────┐
│     BUILD       │
│                 │
│  - Django check │
│  - npm build    │
└────────┬────────┘
         │
         ├──────── develop branch ──────────────┐
         │                                      ▼
         │                            ┌─────────────────┐
         │                            │ DEPLOY STAGING  │
         │                            │                 │
         │                            │ - Railway CLI   │
         │                            │ - Run migrate   │
         │                            └─────────────────┘
         │
         └──────── main branch ─────────────────┐
                                                ▼
                                      ┌─────────────────┐
                                      │ DEPLOY PROD     │
                                      │                 │
                                      │ - Railway CLI   │
                                      │ - Run migrate   │
                                      │ - Notify team   │
                                      └─────────────────┘
```

---

## Setup Instructions

### 1. Railway Setup

**Create environments in Railway:**

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# Create staging environment
# Go to Railway Dashboard → Project → Settings → Environments → Add
```

**Set environment variables in Railway Dashboard:**

| Variable | Staging | Production |
|----------|---------|------------|
| `SECRET_KEY` | staging-key-xxx | prod-key-xxx |
| `DEBUG` | True | False |
| `ALLOWED_HOSTS` | api-staging.xxx | api.xxx |
| `CORS_ALLOWED_ORIGINS` | staging-frontend | prod-frontend |
| `DATABASE_URL` | (auto) | (auto) |

### 2. Netlify Setup

**Connect repository:**
1. Go to Netlify → Add new site → Import from Git
2. Connect GitHub repository
3. Set build settings:
   - Base directory: `client`
   - Build command: `npm run build`
   - Publish directory: `client/build`

**Configure branch deploys:**
1. Site settings → Build & deploy → Branches
2. Production branch: `main`
3. Branch deploys: `develop`
4. Deploy previews: Enabled

**Set environment variables:**

| Context | `REACT_APP_API_URL` |
|---------|---------------------|
| Production | `https://api.yourapp.railway.app` |
| Deploy previews | `https://api-staging.yourapp.railway.app` |
| Branch deploys | `https://api-staging.yourapp.railway.app` |

### 3. GitHub Secrets

Add these secrets in GitHub → Repository → Settings → Secrets:

```
RAILWAY_STAGING_TOKEN    # From Railway dashboard
RAILWAY_PROD_TOKEN       # From Railway dashboard
STAGING_API_URL          # https://api-staging.xxx
PROD_API_URL             # https://api.xxx
NETLIFY_AUTH_TOKEN       # (optional, if using manual deploy)
NETLIFY_SITE_ID          # (optional)
```

---

## Environment Variables Reference

### Backend (.env)

| Variable | Local | Staging | Production |
|----------|-------|---------|------------|
| `SECRET_KEY` | any | unique | unique |
| `DEBUG` | True | True | **False** |
| `ALLOWED_HOSTS` | localhost | staging-domain | prod-domain |
| `DATABASE_URL` | (empty=SQLite) | postgres://... | postgres://... |
| `CORS_ALLOWED_ORIGINS` | localhost:3000 | staging-frontend | prod-frontend |
| `CLOUDINARY_*` | test-creds | staging-creds | prod-creds |
| `OPENAI_API_KEY` | test-key | real-key | real-key |
| `SENDGRID_API_KEY` | - | sandbox | real-key |

### Frontend (.env)

| Variable | Local | Staging | Production |
|----------|-------|---------|------------|
| `REACT_APP_API_URL` | http://localhost:8000/api | https://api-staging.xxx | https://api.xxx |

---

## Quick Commands

```bash
# Deploy to staging manually
git checkout develop
git pull
git push origin develop

# Deploy to production
git checkout main
git merge develop
git push origin main

# Hotfix to production
git checkout main
git checkout -b hotfix/critical-bug
# fix the bug
git push origin hotfix/critical-bug
# Create PR directly to main

# Check deployment status
railway status

# View logs
railway logs --service awfm-backend
```

---

## Monitoring & Rollback

### View Logs

```bash
# Railway
railway logs -f

# Netlify
# Dashboard → Deploys → Functions log
```

### Rollback

**Railway:**
```bash
# Via CLI
railway rollback

# Via Dashboard
# Railway → Deployments → Click on previous → Redeploy
```

**Netlify:**
```
Dashboard → Deploys → Click on previous deploy → Publish deploy
```

---

## Cost Estimate

| Service | Free Tier | Staging | Production |
|---------|-----------|---------|------------|
| Railway | $5/mo credit | ~$3/mo | ~$7/mo |
| Netlify | 100GB bandwidth | $0 | $0 |
| Cloudinary | 25GB | $0 | $0-89/mo |
| GitHub Actions | 2000 min/mo | $0 | $0 |
| **Total** | | **~$3/mo** | **~$7-96/mo** |
