# HIPAA Compliance Guide

## Overview

AWFM handles Protected Health Information (PHI) including:
- User health preferences and care planning decisions
- Video/audio recordings discussing health matters
- Care team communications about health

This document outlines the path from MVP to full HIPAA compliance.

---

## Current vs HIPAA-Compliant Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STACK COMPARISON                                          │
└─────────────────────────────────────────────────────────────────────────────┘

COMPONENT        CURRENT (MVP)              HIPAA-COMPLIANT (Google Cloud)
─────────        ─────────────              ──────────────────────────────

Frontend         Netlify                →   Firebase Hosting (or Vercel)
                 (Free, no BAA)             (BAA included with GCP)

Backend          Railway                →   Google Cloud Run
                 (No BAA)                   (BAA included) ⭐ Easy like Railway

Database         Railway PostgreSQL     →   Google Cloud SQL (PostgreSQL)
                 (No BAA)                   (BAA included) ⭐ Same PostgreSQL

Media Storage    Cloudinary             →   Google Cloud Storage
                 (BAA unclear)              (BAA included) ⭐ Simpler than S3

AI               OpenAI API             →   Vertex AI or Azure OpenAI
                 (No BAA on standard)       (BAA available)

Email            SendGrid Free          →   SendGrid Enterprise
                 (No BAA)                   (BAA available)

MONTHLY COST     ~$7-50                     ~$70-140
```

### Why All-Google Cloud?

| Benefit | Description |
|---------|-------------|
| **One BAA** | Sign once, covers ALL services |
| **Easy setup** | Cloud Run feels like Railway |
| **Same database** | Cloud SQL = PostgreSQL (same as now) |
| **Integrated** | All services work together seamlessly |
| **One bill** | Single invoice, single dashboard |
| **One support** | One place to get help |

---

## HIPAA Requirements Checklist

### Technical Safeguards

| Requirement | Current | HIPAA Target | How to Implement |
|-------------|---------|--------------|------------------|
| Encryption in Transit | ✅ HTTPS | ✅ | Already done (TLS) |
| Encryption at Rest | ✅ Partial | ✅ | Cloud SQL encryption |
| Access Controls | ✅ Django RBAC | ✅ | Already in models |
| Audit Logging | ❌ Missing | ✅ | Add django-auditlog |
| Session Timeout | ❌ Missing | ✅ | Add to settings |
| Auto-Logoff | ❌ Missing | ✅ | Add to frontend |
| Unique User IDs | ✅ UUID | ✅ | Already done |

### Administrative Safeguards

| Requirement | Status | Action Needed |
|-------------|--------|---------------|
| Privacy Policy | ❌ | Draft document |
| Security Policy | ❌ | Draft document |
| Risk Assessment | ❌ | Conduct assessment |
| Staff Training | ❌ | Create training |
| Incident Response Plan | ❌ | Draft plan |
| Business Associate Agreements | ❌ | Sign with all vendors |

### Physical Safeguards

| Requirement | Status | Notes |
|-------------|--------|-------|
| Facility Access | ✅ | Cloud providers handle |
| Workstation Security | N/A | Users responsible |
| Device Controls | ⚠️ | Add device management |

---

## Migration Plan

### Phase 1: Add Security Features (Current Stack)
*Do this NOW while building*

```bash
# Install HIPAA-related packages
pip install django-auditlog
pip install django-encrypted-model-fields
pip install django-axes  # Brute force protection
```

**settings.py additions:**
```python
# Session Security
SESSION_COOKIE_AGE = 900  # 15 minutes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Password Requirements
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Audit Logging
INSTALLED_APPS += ['auditlog']

# Brute Force Protection
INSTALLED_APPS += ['axes']
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # 1 hour lockout
```

### Phase 2: Migrate to HIPAA-Compliant Hosting
*Before going to production with real patients*

```
Week 1: Set up Google Cloud
─────────────────────────────
□ Create GCP account
□ Enable Cloud Run, Cloud SQL, Cloud Storage
□ Sign Google Cloud BAA (covers ALL services)
□ Deploy backend to Cloud Run
□ Migrate database to Cloud SQL

Week 2: Migrate Media & AI
─────────────────────────────
□ Set up Cloud Storage bucket with encryption
□ Migrate media from Cloudinary to Cloud Storage
□ Set up Vertex AI (Google's AI) or Azure OpenAI
□ Switch from OpenAI API to HIPAA-compliant AI

Week 3: Frontend & Email
─────────────────────────────
□ Deploy frontend to Firebase Hosting (or Vercel Enterprise)
□ Upgrade SendGrid to Enterprise
□ Sign SendGrid BAA

Week 4: Audit & Documentation
─────────────────────────────
□ Conduct security audit
□ Complete risk assessment
□ Finalize privacy policy
□ Document all procedures
□ Test incident response
```

---

## HIPAA-Compliant Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HIPAA-COMPLIANT ARCHITECTURE (All Google Cloud)           │
└─────────────────────────────────────────────────────────────────────────────┘

                         USERS
                           │
                           ▼
                  ┌─────────────────┐
                  │ Cloud Armor     │ ← DDoS Protection (included)
                  │ Load Balancer   │
                  └────────┬────────┘
                           │
         ┌─────────────────┴─────────────────┐
         ▼                                   ▼
┌─────────────────┐                 ┌─────────────────┐
│    Firebase     │                 │  Google Cloud   │
│    Hosting      │                 │      Run        │
│                 │                 │                 │
│  React Frontend │                 │  Django Backend │
│  (BAA included) │                 │  (BAA included) │
└─────────────────┘                 └────────┬────────┘
                                             │
                    ┌────────────────────────┼────────────────────────┐
                    │                        │                        │
                    ▼                        ▼                        ▼
           ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
           │  Google Cloud   │     │  Google Cloud   │     │   Vertex AI     │
           │      SQL        │     │    Storage      │     │   (or Azure)    │
           │                 │     │                 │     │                 │
           │  PostgreSQL     │     │  Video/Audio    │     │  AI Features    │
           │  (encrypted)    │     │  Storage        │     │  (Gemini/GPT-4) │
           │  (BAA included) │     │  (encrypted)    │     │                 │
           │                 │     │  (BAA included) │     │  (BAA included) │
           └─────────────────┘     └─────────────────┘     └─────────────────┘
                    │
                    ▼
           ┌─────────────────┐
           │  Google Cloud   │
           │  Audit Logs     │ ← All access logged automatically
           └─────────────────┘

⭐ ONE BAA covers ALL services above (except Azure if used)
```

---

## Business Associate Agreements (BAAs)

### What is a BAA?

A legal contract where the vendor agrees to:
- Protect your PHI
- Only use it as directed
- Report any breaches
- Follow HIPAA rules

### BAAs You'll Need

| Vendor | Service | How to Get BAA |
|--------|---------|----------------|
| Google Cloud | Backend, Database, Storage, Frontend, AI | **ONE BAA** - automatic in settings |
| SendGrid | Email | Upgrade to Enterprise |

### How to Sign

**Google Cloud (Recommended - ONE BAA for everything):**
```
1. Go to Console → IAM & Admin → Settings
2. Accept Google Cloud BAA
3. Done! ✅ This covers:
   - Cloud Run (backend)
   - Cloud SQL (database)
   - Cloud Storage (media)
   - Firebase Hosting (frontend)
   - Vertex AI (if using Google AI)
   - Cloud Audit Logs
   - ALL other GCP services
```

**SendGrid:**
```
1. Upgrade to Enterprise plan
2. Contact SendGrid sales for BAA
3. Sign BAA
```

**Azure (only if using Azure OpenAI instead of Vertex AI):**
```
1. Go to Trust Center
2. Find Business Associate Agreement
3. Accept for your subscription
4. Done
```

---

## Required Policies & Documents

### 1. Privacy Policy
Must include:
- What PHI you collect
- How you use it
- Who you share it with
- User rights (access, correction, deletion)
- How to file complaints

### 2. Security Policy
Must include:
- Access control procedures
- Password requirements
- Encryption standards
- Incident response procedures
- Employee training requirements

### 3. Risk Assessment
Document:
- All systems that handle PHI
- Potential threats
- Likelihood and impact
- Mitigation measures

---

## Audit Logging Requirements

### What to Log

```python
# All PHI access must be logged:

AUDIT_EVENTS = [
    'user_login',
    'user_logout',
    'user_login_failed',
    'phi_viewed',           # Someone viewed health data
    'phi_created',          # Someone created health data
    'phi_updated',          # Someone modified health data
    'phi_deleted',          # Someone deleted health data
    'phi_exported',         # Someone downloaded/exported
    'explanation_viewed',   # Care team viewed recording
    'explanation_shared',   # Recording shared
    'team_member_added',    # New person given access
    'team_member_removed',  # Access revoked
]
```

### Log Retention

- Minimum: 6 years
- Recommended: 7 years
- Must be tamper-proof

---

## Incident Response Plan

### If a Breach Occurs

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BREACH RESPONSE TIMELINE                                  │
└─────────────────────────────────────────────────────────────────────────────┘

IMMEDIATELY (Within hours)
─────────────────────────
□ Contain the breach (revoke access, patch vulnerability)
□ Document everything
□ Notify security team

WITHIN 24 HOURS
─────────────────────────
□ Assess scope (what data, how many affected)
□ Preserve evidence
□ Begin investigation

WITHIN 60 DAYS (Required by law)
─────────────────────────
□ Notify affected individuals
□ Notify HHS (if 500+ affected)
□ Notify media (if 500+ in one state)

ONGOING
─────────────────────────
□ Complete investigation
□ Implement fixes
□ Update policies
□ Document lessons learned
```

---

## Cost Comparison

### MVP Phase (Current)

| Service | Monthly Cost |
|---------|--------------|
| Railway | ~$7 |
| Netlify | $0 |
| Cloudinary | $0-89 |
| OpenAI | ~$10-50 |
| **Total** | **~$17-150** |

### HIPAA-Compliant Phase (All Google Cloud)

| Service | Monthly Cost |
|---------|--------------|
| Google Cloud Run | ~$20-40 |
| Google Cloud SQL | ~$15-30 |
| Google Cloud Storage | ~$5-15 |
| Vertex AI (or Azure OpenAI) | ~$10-50 |
| Firebase Hosting | ~$0-25 |
| SendGrid Enterprise | ~$15 |
| **Total** | **~$65-175** |

⭐ **Bonus**: All Google services on ONE invoice, ONE dashboard, ONE support team!

### Additional Costs

| Item | One-Time Cost |
|------|---------------|
| Security Audit | $2,000-10,000 |
| Legal Review (policies) | $1,000-5,000 |
| Penetration Testing | $3,000-15,000 |
| Staff Training | $500-2,000 |

---

## Timeline to Compliance

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HIPAA COMPLIANCE TIMELINE                                 │
└─────────────────────────────────────────────────────────────────────────────┘

NOW                          3 MONTHS                      6 MONTHS
───                          ────────                      ────────

Build MVP                    Migrate hosting              Full compliance
Add audit logging            Sign BAAs                    Security audit
Add session security         Draft policies               Penetration test
Test with fake data          Risk assessment              Go live with PHI
                             Staff training

[──────────────────]         [──────────────────]         [──────────────]
   Development                  Migration                   Production
```

---

## Checklist Summary

### Before MVP Launch (Test Users)
- [ ] Add django-auditlog
- [ ] Add session timeouts
- [ ] Add password requirements
- [ ] Add brute force protection
- [ ] Use test data only (no real PHI)

### Before Production (Real Patients)
- [ ] Create Google Cloud account
- [ ] Sign Google Cloud BAA (covers everything!)
- [ ] Migrate backend to Google Cloud Run
- [ ] Migrate database to Google Cloud SQL
- [ ] Migrate media to Google Cloud Storage
- [ ] Set up Vertex AI (or Azure OpenAI)
- [ ] Deploy frontend to Firebase Hosting
- [ ] Upgrade SendGrid to Enterprise + sign BAA
- [ ] Complete risk assessment
- [ ] Draft privacy policy
- [ ] Draft security policy
- [ ] Conduct security audit
- [ ] Train staff
- [ ] Document incident response plan

---

## Resources

- [HHS HIPAA Guidelines](https://www.hhs.gov/hipaa/index.html)
- [Google Cloud HIPAA Compliance](https://cloud.google.com/security/compliance/hipaa)
- [Google Cloud Healthcare API](https://cloud.google.com/healthcare-api)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres)
- [Cloud Storage Documentation](https://cloud.google.com/storage/docs)
- [Firebase Hosting](https://firebase.google.com/docs/hosting)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Azure HIPAA Compliance](https://docs.microsoft.com/en-us/azure/compliance/offerings/offering-hipaa-us) (if using Azure OpenAI)
- [Django Security Best Practices](https://docs.djangoproject.com/en/4.2/topics/security/)
