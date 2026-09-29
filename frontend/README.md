# NexStep Frontend

React + Vite + Tailwind frontend for NexStep.

The frontend is wired to the FastAPI backend rather than local mock data. Student and admin
sessions use separate JWT storage, and the admin extraction/review screens call the backend
AI discovery and human-review endpoints directly.

## Run it

```bash
npm install
npm run dev
```

The Vite development server runs at `http://localhost:5173` by default.

Set `VITE_API_BASE_URL` in `.env` when the backend is not running at the default
`http://localhost:8000/api`.

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## Build

```bash
npm run build
```

## Main frontend areas

```text
src/
├── api/                 Student API clients
├── admin/               Admin app, API clients, pages and review components
├── components/          Shared UI, layout and assistant components
├── context/             Authentication, profile and notification state
├── pages/               Student-facing screens
├── routes/              Student route guards
└── utils/               Shared helpers
```

## Backend integrations

Student:

- `/api/auth/*` — authentication and current user
- `/api/student/profile` — profile read/write
- `/api/exams` — approved exams and search
- `/api/eligibility/*` — eligibility evaluation
- `/api/notifications/*` — student notifications
- `/api/assistant/chat` — retrieval-grounded assistant

Admin:

- `/api/auth/admin/login` and `/api/auth/*` — admin authentication
- `/admin/extractions` — AI discovery and extraction history
- `/admin/extractions/{id}` — extraction review data
- `/admin/extractions/{id}/approve` — approve extraction
- `/admin/extractions/{id}/reject` — reject extraction
- `/admin/extractions/{id}/retry` — retry rejected extraction
- `/api/exams` — authoritative approved exam data

The admin discovery pipeline is executed by the backend. The frontend does not simulate
processing stages or maintain an in-memory extraction database.
