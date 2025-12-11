# AWFM Technology Overview (Simplified)

**What users can do:**
- Answer 30 questions about their healthcare wishes
- Record video, audio, or text explanations for their answers
- Invite family members and caregivers to view their preferences
- Get help from AI to understand and summarize their choices

---

## How Does the App Work? (Simple Explanation)

Think of AWFM like a house with different rooms:

```
THE AWFM "HOUSE"
================

    [FRONT DOOR]           [BACK OFFICE]           [STORAGE]
    What you see           Behind the scenes       Where stuff is kept
    ────────────           ─────────────────       ──────────────────

    Website &              The "brain" that        - User accounts
    buttons you            processes your          - Questions & answers
    click on               requests                - Videos & recordings
                                                   - Care team info
```

| Part | What It Does | Real-World Analogy |
|------|--------------|-------------------|
| **Frontend** | The screens and buttons you see | The storefront of a shop |
| **Backend** | Processes your actions (login, save, etc.) | The employees working behind the counter |
| **Database** | Stores all your information | Filing cabinets that organize everything |
| **Media Storage** | Stores your videos and audio recordings | A secure vault for valuable items |

---

## Proposed Tech Stack

### The Website You See (Frontend)

| Platform | What It Is | Why This |
|-------------|-----------|-----------------|
| **React** | A tool for building websites | Used by Facebook, Netflix, Airbnb - very reliable |
| **Netlify** | Where the website lives | Free to start, very fast for users |

**Cost:** Free (for now)

---

### Backend Framework

| Platform | What It Is | Why This |
|-------------|-----------|-----------------|
| **Django** | A system that handles all the logic | Like a well-organized office manager |
| **Railway** | Where our backend lives | Easy to use, affordable |

**Why Django?**
- It's been around for 18+ years (very trustworthy)
- Comes with built-in security features
- Easy to add new features
- Works great with AI tools

**Cost:** ~$5-10/month

---

### Database

| Platform | What It Is | Why This |
|-------------|-----------|-----------------|
| **PostgreSQL** | A database | Industry standard, very reliable |

**Why PostgreSQL over alternatives?**

Your data has relationships:
- A **user** has a **care team**
- A care team has **members**
- Members can **react** to **explanations**

PostgreSQL is perfect for this kind of connected data.

**Cost:** Included with Railway

---

### Where Your Videos Are Stored (Media Storage)

| Platform | What It Is | Why This |
|-------------|-----------|-----------------|
| **Cloudinary** | A service that stores and delivers videos/audio | Handles all the complex video stuff for us |

**Why Cloudinary?**
- Automatically makes videos play smoothly on any device
- Creates thumbnails automatically
- Fast delivery worldwide
- Simple to set up

**Cost:** Free up to 25GB, then ~$89/month

---

### Proposed AI Integration (Could be done POST MVP)

| Platform | What It Is | Why This |
|-------------|-----------|-----------------|
| **OpenAI or Claude** | Artificial intelligence | Best at understanding and summarizing text |

**What the AI does:**
- Summarizes explanations
- Compares different family members' views
- Helps explain medical terms in simple language

**Cost:** ~$10-50/month (depends on usage)

---

## Total Monthly Costs

### Starting Out (MVP Phase)

| Service | Monthly Cost |
|---------|--------------|
| Website hosting (Netlify) | Free |
| Backend + Database (Railway) | ~$5-10 |
| Video storage (Cloudinary) | Free - $89 |
| AI features (OpenAI) | ~$10-50 | **Tentative
| Email sending (SendGrid) | Free |
| **TOTAL** | **~$15-150/month** |

### When Handling Real Patient Data (HIPAA Phase)

| Service | Monthly Cost |
|---------|--------------|
| Google Cloud (everything) | ~$40-85 |
| AI features | ~$10-50 |
| Email sending | ~$15 |
| **TOTAL** | **~$65-175/month** |

---

### The Key HIPAA Requirements 

| Requirement | What It Means | How We Handle It |
|-------------|---------------|------------------|
| **Encryption** | Scramble data so hackers can't read it | All data is encrypted automatically |
| **Access Control** | Only authorized people can see data | Users control who's in their care team |
| **Audit Logs** | Keep records of who viewed what | System logs all access automatically |
| **BAA (Business Associate Agreement)** | Legal contract with our vendors | We sign agreements with Google Cloud, etc. |
| **Session Timeout** | Auto-logout after inactivity | App logs you out after 15 minutes |

### What is a BAA?

A **Business Associate Agreement** is like a contract where a company promises:

> "We will protect your users' health data. If there's ever a breach, we'll tell you immediately. We follow all HIPAA rules."

**Without a BAA, we can't legally store health data with that company.**

---

## Proposed HIPAA Compliance Plan

### Phase 1: Building the App (NOW)
- Use test data only (no real patient information)
- Build all the security features
- Cost: ~$15-150/month

### Phase 2: Going Live with Real Patients (LATER)
- Move everything to Google Cloud (they sign BAAs)
- Complete security audit
- Create privacy policies
- Cost: ~$65-175/month + one-time costs

### Why Google Cloud for HIPAA?

| Benefit | What It Means For You |
|---------|----------------------|
| **One Agreement** | Sign ONE contract, covers everything |
| **One Bill** | Single invoice each month |
| **One Support Team** | One phone number to call for help |
| **Easy Migration** | Similar to what we use now |

---

## Timeline Overview

```
NOW                     3 MONTHS                 6 MONTHS
───                     ────────                 ────────

Build the app           Move to Google Cloud     Go live with
with test data          Sign legal agreements    real patients
                        Security testing

FREE - $150/mo          $65-175/mo               $65-175/mo
                        + one-time costs         (ongoing)
```

## Common Questions

### "Is our data safe?"

**Yes.** We use:
- Encrypted connections (like online banking)
- Secure passwords with lockout protection
- All data stored with HIPAA-compliant companies

### "Who can see my information?"

Only people YOU invite to your care team. You control:
- Who gets invited
- What they can see
- When to remove someone

### "What happens if there's a security breach?"

We have a response plan:
1. Immediately contain the issue
2. Notify affected users within 60 days (required by law)
3. Report to government if 500+ people affected
4. Fix the problem and improve security

### "Can I delete my data?"

Yes. Users can request complete deletion of their account and all associated data.

### "Where is my data stored?"

Currently: Railway servers (US-based)
After HIPAA migration: Google Cloud servers (US-based, HIPAA-certified)

---

## Glossary

| Term | Simple Definition |
|------|-------------------|
| **API** | A way for different software to talk to each other |
| **Backend** | The part of the app you don't see (processes your requests) |
| **BAA** | Legal contract promising to protect health data |
| **Cloud** | Computers owned by Google/Amazon/etc. that we rent |
| **Database** | Where all the information is organized and stored |
| **Encryption** | Scrambling data so only authorized people can read it |
| **Frontend** | The part of the app you see and interact with |
| **HIPAA** | US law protecting health information |
| **MVP** | Minimum Viable Product - the first basic version |
| **PHI** | Protected Health Information - health data covered by HIPAA |
| **Server** | A computer that runs our app 24/7 |

---

## Summary

```
AWFM TECHNOLOGY IN ONE PAGE
===========================


HOW IT WORKS:
Website (React) → Backend Brain (Django) → Database (PostgreSQL)
                                        → Video Storage (Cloudinary)
                                        → AI Features (OpenAI)

COST TO RUN:
Starting: $15-150/month
With HIPAA compliance: $65-175/month

SECURITY:
- All data encrypted
- User-controlled access
- HIPAA compliant when handling real patients
- Regular security audits

TIMELINE:
Build now → Test with fake data → Security review → Go live with real patients
```

---
