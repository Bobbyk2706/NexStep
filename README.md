# NexStep

### AI-Powered Exam Eligibility and Tracking Platform

NexStep helps students discover examinations they are eligible for, track important deadlines, and receive updates from official examination sources.

It combines **AI, automation, and rule-based eligibility evaluation** to provide personalized examination information in one place.

---

## Features

### Student

- Registration & Login
- Student Profile
- Automatic Exam Eligibility Checking
- Eligible / Non-Eligible Exams
- Exam Tracking
- Deadline Reminders
- In-App & Email Notifications
- AI Chat Assistant

### Admin

- Manage Examinations
- Manage Eligibility Rules
- Review AI-extracted information
- Approve / Reject updates
- Audit Logs

### Automation & AI

- Monitor official examination websites
- Detect new and updated notifications
- Extract information from official notifications
- Compare notification versions
- Summarize important updates
- Trigger eligibility re-evaluation and notifications

---

## Technology Stack

- **Frontend:** React, JavaScript, HTML, CSS
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **AI:** Large Language Models
- **Automation:** Selenium, BeautifulSoup
- **Authentication:** JWT
- **Tools:** Git, GitHub, VS Code

---

## Development Status

**Current Phase:** Architecture & Development

### Completed

- Requirements Analysis
- SRS
- SADD
- System Architecture
- ER Diagram
- Database Design
- Initial PostgreSQL Tables & Relationships

### Next

- Backend Development
- Authentication
- Eligibility Engine
- Frontend Development
- Automation
- AI Integration
- Notifications
- Testing & Deployment

---
## Goal

NexStep aims to transform examination discovery from a **manual search process** into a **personalized and automated service**.

> **Instead of searching multiple websites to find opportunities, students can find the examinations they are eligible for in one place.**

---

# Project Structure

```text
NexStep/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── database/
│   │   ├── auth/
│   │   ├── eligibility/
│   │   ├── notifications/
│   │   ├── automation/
│   │   └── ai/
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   │
│   └── package.json
│
├── database/
│   ├── schema/
│   └── migrations/
│
├── docs/
│   ├── SRS/
│   ├── SADD/
│   └── diagrams/
│
├── tests/
│   ├── backend/
│   ├── frontend/
│   └── integration/
│
├── .gitignore
└── README.md
