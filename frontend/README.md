# NexStep — Frontend

A React (Vite + Tailwind) frontend for NexStep: students fill in their profile once, and NexStep
<<<<<<< HEAD
automatically shows which exams they're eligible for — no picking an exam first. Visual identity
is a restrained academic-luxury system (warm ink/ivory/antique-gold, serif+sans+mono type) shared
across the student app, admin console, and the assistant feature.
=======
automatically shows which exams they're eligible for — no picking an exam first.
>>>>>>> origin/main

## Run it

```bash
npm install
npm run dev
```

Opens at `http://localhost:5173`. Sign up with any name/email and a 6+ character password —
auth is mocked, so nothing needs to be running on a backend yet.

`npm run build` produces a production build in `dist/`.

<<<<<<< HEAD
## Design system

**Concept:** the same "scholarly reading room" language as NexStep's sibling luxury build —
warm ink on warm ivory, one antique-gold accent reserved for hairlines/links/citations, restrained
radii (capped at 10px), and hairline borders doing the depth work that shadows do elsewhere. Every
color in the app comes from the token table below — verified by grepping for stray default
Tailwind colors, not just eyeballed.

| Token | Value | Use |
|---|---|---|
| `ink` | `#1A1815` | Primary text, primary buttons |
| `ink.soft` | `#57534A` | Secondary text |
| `paper` | `#F7F3EC` | Page background |
| `surface` | `#FBF9F5` | Raised card/button surfaces |
| `slate-*` | warm taupe ramp | Recessed surfaces (inputs, nested rows), muted text — `slate.400/500` verified at ≥4.5:1 against `paper` |
| `indigo-700` | `#1A1815` (= ink) | Solid button fills — kept under the old name so every `bg-indigo-700` repaints automatically |
| `gold` | `#8A6A34` | Link/accent text, focus rings, citation numbers — link/accent text was redirected here specifically so it doesn't disappear into `indigo-700`'s ink value |
| `signal` | deep forest | Eligible / approved |
| `amber` | deep ochre | Attention / closing-soon |
| `red` (admin) | muted rust | Rejected / failed |

Fonts: **Newsreader** (serif, headings), **General Sans** (UI/body), **IBM Plex Mono** (citation
numbers, metadata, status tags).

The eligibility indicator (`components/ui/EligibilityPill.jsx`) and its admin sibling
(`admin/components/StatusBadge.jsx`) were redesigned from filled rounded-full pills to bordered
tags — reads as a printed label rather than a SaaS status chip, and it's the one visual element
that repeats across nearly every screen, so it was worth getting right by hand rather than just
recoloring the old shape.

=======
>>>>>>> origin/main
## What's implemented

- **Landing page** — intro, features, sign up / log in
- **Signup & Login** — client-side validation, error states
- **Student profile** — personal + academic details, repeatable qualifications and work
  experience, conditional Master's/PhD "previous qualification" fields
- **Dashboard** — student name, exam counts, upcoming deadlines, recent notifications, quick links
<<<<<<< HEAD
- **Assistant** (`/assistant`, new) — see below
=======
>>>>>>> origin/main
- **Eligibility results** — automatic, filtered list (Eligible / Not eligible / All) — the student
  never selects an exam first
- **Exam details** — full info per exam, including why the student is/isn't eligible
- **Upcoming exams/deadlines** — timeline of eligible exams' application windows and exam dates
- **Notifications** — deadline, exam date, newly-eligible, and update types, with read/unread state
- **Search/browse exams** — by name, organization, or category
- **Profile/settings** — view, edit, log out

<<<<<<< HEAD
## The Assistant (`/assistant`)

A chat interface for asking about exams in plain language, personalized against the student's
*actual* saved profile and computed eligibility rather than generic text — ask "Am I eligible for
GATE?" and it answers using the same `computeEligibility` result the Eligibility page shows, with
sources citing the specific exam rule and the student's own profile.

- Suggested questions on the empty state; answers stream through a calm "thinking" state
- Every required non-happy-path state is implemented: no relevant information found,
  backend/reasoning-service unavailable, and network error — each a quiet in-palette banner
- A small "Preview:" switcher in the input area forces the next answer into any of those states on
  demand, since there's no real backend to trigger them naturally — it's a demo/review affordance
  documented here so it isn't mistaken for a real feature; remove it once this connects to an
  actual backend
- Answer matching lives in `src/data/assistantKnowledge.js` (`findAnswer`) — kept deliberately
  simple (keyword matching, single-thread conversation, no persisted history) given this sits
  alongside a much larger admin/student surface; swap `findAnswer` for a real API call when ready

=======
>>>>>>> origin/main
## Project structure

```
src/
<<<<<<< HEAD
  admin/          Admin portal — self-contained (own api/, context/, routes/, components/, pages/)
                  Reuses src/components/ui/* and src/utils/date.js for visual consistency.
=======
>>>>>>> origin/main
  api/            Mock API layer — the ONLY place that needs to change to plug in Vivek's backend
    client.js       fetch wrapper (JWT header injection, error handling) — already set up for real use
    auth.js         login / signup — replace mock bodies with request() calls (see comments inline)
    profile.js      get / save student profile
    exams.js        exam list + eligibility engine (computeEligibility) + search
    notifications.js
    mockData.js     seed data standing in for real API responses
<<<<<<< HEAD
  data/
    assistantKnowledge.js   Assistant's answer matching — see above
=======
>>>>>>> origin/main
  context/        React context — Auth, Profile+Exams, Notifications
  routes/         Route guards (RequireAuth, RequireProfile)
  components/
    ui/             Button, Card, Field (Text/Select/Textarea), EligibilityPill, Logo
    layout/         PublicNavbar (landing/login/signup), AppShell (sidebar/bottom-nav for the app)
<<<<<<< HEAD
    chat/           Assistant's UI: MessageBubble, MessageInput, SourcesPanel, StateBanner, EmptyState
  pages/          One file per screen
```

## Admin portal

A separate admin console lives under `/admin/*` (`src/admin/`), sharing the same design tokens,
components, and build as the student app but with its own login, auth session, and layout — the
two never mix. Log in at `/admin/login` (same mock rule: any 6+ character password).

- **Dashboard** (`/admin/dashboard`) — pending/approved/rejected/failed counts, recent activity
- **Add Exam** (`/admin/exams/new`) — admin provides only the exam name; everything else (source,
  dates, eligibility rules) is discovered/extracted automatically
- **AI Processing** — after starting discovery, the same page shows a live checklist through the
  real backend pipeline stages (source discovery → verification → download → extraction →
  chunking → AI extraction → aggregation → normalization → validation → review), simulated with a
  mock ticker in `advanceProcessing()` until a real backend reports status
- **Review** (`/admin/extractions/:id`) — source info, exam info, eligibility info, a **recursive**
  eligibility rule tree (nested AND/OR groups, never flattened), evidence/provenance per field,
  conflict detection (never auto-resolves — shows both values with sources), validation issues,
  and Approve / Reject (feedback required) / Retry (creates a new version, keeps history)
- **Extraction History** (`/admin/extractions`) — filterable by status, searchable by exam name
- **All Exams / Exam Details** (`/admin/exams`, `/admin/exams/:examId`) — authoritative approved data

Try the full loop: Add Exam → watch it process → Reject with feedback → open the rejected
extraction → Retry → watch it process again → Approve → land on the exam's authoritative detail
page. The flagship "Civil Services Examination 2026" extraction in the mock data ships with a
conflict and validation issues already populated so you can see those panels without waiting.

=======
  pages/          One file per screen
```

>>>>>>> origin/main
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

<<<<<<< HEAD
## Review pass

This redesign went through the same three passes as the design brief called for: a **luxury**
pass (grepped for stray default-Tailwind colors, `rounded-full` on anything larger than a small
dot/icon button, and default `shadow-lg/xl` — found and fixed a couple of leftover filled-pill
badges and swapped two default-black modal shadows for the palette's warm-tinted one), a **UX**
pass (fixed a same-tone collision where nested rule-tree rows were becoming invisible against
their own container once both moved to the same recycled token — see `surface` vs `slate-*` in
the table above), and an **accessibility** pass on contrast (caught `slate-400` text sitting
directly on the dark admin sidebar at ~2.8:1 — far under the 4.5:1 needed — and moved those
specific instances to `slate-300`, which clears 9:1 against the sidebar's near-black).
=======
## Design notes

- Color and type tokens live in `tailwind.config.js` (indigo/signal-green/amber palette,
  Clash Display + Satoshi + JetBrains Mono).
- The eligibility "pill" (`components/ui/EligibilityPill.jsx`) is the one repeating visual
  language across the app — filled green for eligible, amber when a deadline is within 14 days,
  outlined gray for not eligible.
- Sidebar nav on desktop, bottom tab bar on mobile (`components/layout/AppShell.jsx`).
>>>>>>> origin/main
