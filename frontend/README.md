# NexStep — Frontend

A React (Vite + Tailwind) frontend for NexStep: students fill in their profile once, and NexStep
automatically shows which exams they're eligible for — no picking an exam first.

## Run it

```bash
npm install
npm run dev
```

Opens at `http://localhost:5173`. Sign up with any name/email and a 6+ character password —
auth is mocked, so nothing needs to be running on a backend yet.

`npm run build` produces a production build in `dist/`.

## What's implemented

- **Landing page** — intro, features, sign up / log in
- **Signup & Login** — client-side validation, error states
- **Student profile** — personal + academic details, repeatable qualifications and work
  experience, conditional Master's/PhD "previous qualification" fields
- **Dashboard** — student name, exam counts, upcoming deadlines, recent notifications, quick links
- **Eligibility results** — automatic, filtered list (Eligible / Not eligible / All) — the student
  never selects an exam first
- **Exam details** — full info per exam, including why the student is/isn't eligible
- **Upcoming exams/deadlines** — timeline of eligible exams' application windows and exam dates
- **Notifications** — deadline, exam date, newly-eligible, and update types, with read/unread state
- **Search/browse exams** — by name, organization, or category
- **Profile/settings** — view, edit, log out

## Project structure

```
src/
  api/            Mock API layer — the ONLY place that needs to change to plug in Vivek's backend
    client.js       fetch wrapper (JWT header injection, error handling) — already set up for real use
    auth.js         login / signup — replace mock bodies with request() calls (see comments inline)
    profile.js      get / save student profile
    exams.js        exam list + eligibility engine (computeEligibility) + search
    notifications.js
    mockData.js     seed data standing in for real API responses
  context/        React context — Auth, Profile+Exams, Notifications
  routes/         Route guards (RequireAuth, RequireProfile)
  components/
    ui/             Button, Card, Field (Text/Select/Textarea), EligibilityPill, Logo
    layout/         PublicNavbar (landing/login/signup), AppShell (sidebar/bottom-nav for the app)
  pages/          One file per screen
```

## Connecting Vivek's API

1. Set `VITE_API_BASE_URL` in a `.env` file (see `.env.example`) to the real API's base URL.
2. In each `src/api/*.js` file, there's a comment showing the `request(...)` call that should
   replace the mock body — the function signatures and return shapes are already designed to
   match, so pages/components shouldn't need to change.
3. `client.js` already stores the JWT in `localStorage` and attaches it as a `Bearer` token on
   every request — `setToken()` / `getToken()` are ready to use as-is.
4. The eligibility logic in `exams.js` (`computeEligibility`) is a placeholder rule set. Once
   there's a real eligibility endpoint, swap `getExams`/`getExamById` to call it directly instead
   of computing rules client-side.

## Design notes

- Color and type tokens live in `tailwind.config.js` (indigo/signal-green/amber palette,
  Clash Display + Satoshi + JetBrains Mono).
- The eligibility "pill" (`components/ui/EligibilityPill.jsx`) is the one repeating visual
  language across the app — filled green for eligible, amber when a deadline is within 14 days,
  outlined gray for not eligible.
- Sidebar nav on desktop, bottom tab bar on mobile (`components/layout/AppShell.jsx`).
