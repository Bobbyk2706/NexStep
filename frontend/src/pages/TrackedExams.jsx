// Tracked Exams — single-file feature for NexStep.
//
// Place at: frontend/src/pages/TrackedExams.jsx
//
// Exports
//   default            <TrackedExams />   the "Tracked exams" page
//   TrackButton        <TrackButton examId={...} />   Track / Untrack action
//   useTrackedExams()  hook: { records, trackedIds, status, error, ... }
//
// Backend contract (already implemented, mounted under /api):
//   GET    /tracked-exams               -> [{ tracking_id, exam_id, tracked_at, ... }]
//   POST   /tracked-exams/{exam_id}     -> { tracking_id, exam_id, ... }  (409 if already tracked)
//   DELETE /tracked-exams/{tracking_id} -> 204                            (note: tracking_id, not exam_id)
//
// The backend list is the source of truth, so tracking survives refresh and
// logout/login. A small module-level store keeps every TrackButton and the
// page in sync without needing a new provider in App.jsx. It resets and
// reloads automatically when the signed-in user changes.

import { useCallback, useEffect, useState, useSyncExternalStore } from "react";
import { Link } from "react-router-dom";
import { Bookmark, BookmarkCheck, RefreshCw } from "lucide-react";
import Button from "../components/ui/Button";
import Card from "../components/ui/Card";
import { request } from "../api/client";
import { getExamById } from "../api/exams";
import { useAuth } from "../context/AuthContext";
import { formatDate, timeAgo } from "../utils/date";

/* ----------------------------------------------------------------------------
 * API
 * ------------------------------------------------------------------------- */

const trackedExamsApi = {
  list: () => request("/tracked-exams"),
  track: (examId) =>
    request(`/tracked-exams/${encodeURIComponent(examId)}`, { method: "POST" }),
  untrack: (trackingId) =>
    request(`/tracked-exams/${encodeURIComponent(trackingId)}`, {
      method: "DELETE",
    }),
};

/* ----------------------------------------------------------------------------
 * Shared store (module level, consumed through useSyncExternalStore)
 * ------------------------------------------------------------------------- */

const EMPTY_STATE = {
  owner: undefined, // identity the data belongs to (user email) — undefined = never loaded
  status: "idle", // idle | loading | ready | error
  error: "",
  records: [], // [{ tracking_id, exam_id, tracked_at, tracking_status }]
  pending: [], // exam ids with an in-flight track/untrack call
};

let state = EMPTY_STATE;
let loadToken = 0; // invalidates stale list responses
const listeners = new Set();

function setState(patch) {
  state = { ...state, ...patch };
  listeners.forEach((listener) => listener());
}

function subscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

function getState() {
  return state;
}

function sortRecords(records) {
  return [...records].sort(
    (a, b) => new Date(b.tracked_at || 0) - new Date(a.tracked_at || 0)
  );
}

function toRecord(raw) {
  return { ...raw, exam_id: Number(raw.exam_id) };
}

async function loadRecords() {
  const token = ++loadToken;
  setState({ status: "loading", error: "" });

  try {
    const data = await trackedExamsApi.list();
    if (token !== loadToken) return;

    setState({
      status: "ready",
      error: "",
      records: sortRecords((data || []).map(toRecord)),
    });
  } catch (err) {
    if (token !== loadToken) return;

    setState({
      status: "error",
      error: err?.message || "Could not load your tracked exams.",
    });
  }
}

// Called by the hook. Resets the store when the signed-in user changes.
function syncOwner(owner) {
  if (state.owner !== owner) {
    loadToken++; // drop any response that belongs to the previous user
    state = { ...EMPTY_STATE, owner };

    if (owner) {
      loadRecords();
    } else {
      state = { ...state, status: "ready" };
      listeners.forEach((listener) => listener());
    }
    return;
  }

  if (owner && state.status === "idle") {
    loadRecords();
  }
}

function setPending(examId, on) {
  const rest = state.pending.filter((id) => id !== examId);
  setState({ pending: on ? [...rest, examId] : rest });
}

async function trackExam(examIdRaw) {
  const examId = Number(examIdRaw);

  if (!Number.isFinite(examId)) {
    return { ok: false, message: "Invalid exam." };
  }
  if (state.pending.includes(examId)) {
    return { ok: false, message: "Please wait…" };
  }
  if (state.records.some((r) => r.exam_id === examId)) {
    return { ok: true, message: "Already tracking this exam." };
  }

  setPending(examId, true);

  try {
    const record = toRecord(await trackedExamsApi.track(examId));

    setState({
      records: sortRecords([
        ...state.records.filter((r) => r.exam_id !== examId),
        record,
      ]),
    });
    return { ok: true, message: "Exam added to your tracked list." };
  } catch (err) {
    if (err?.status === 409) {
      // Tracked elsewhere (another tab/device) — just re-sync.
      await loadRecords();
      return { ok: true, message: "Already tracking this exam." };
    }
    return { ok: false, message: err?.message || "Could not track this exam." };
  } finally {
    setPending(examId, false);
  }
}

async function untrackExam(examIdRaw) {
  const examId = Number(examIdRaw);
  const record = state.records.find((r) => r.exam_id === examId);

  if (!record) {
    return { ok: true, message: "This exam is not tracked." };
  }
  if (state.pending.includes(examId)) {
    return { ok: false, message: "Please wait…" };
  }

  setPending(examId, true);

  try {
    await trackedExamsApi.untrack(record.tracking_id);

    setState({ records: state.records.filter((r) => r.exam_id !== examId) });
    return { ok: true, message: "Exam removed from your tracked list." };
  } catch (err) {
    if (err?.status === 404) {
      // Already gone on the server — just re-sync.
      await loadRecords();
      return { ok: true, message: "This exam is not tracked." };
    }
    return { ok: false, message: err?.message || "Could not untrack this exam." };
  } finally {
    setPending(examId, false);
  }
}

/* ----------------------------------------------------------------------------
 * Hook
 * ------------------------------------------------------------------------- */

export function useTrackedExams() {
  const { user } = useAuth();
  const owner = user?.email ?? null;
  const snapshot = useSyncExternalStore(subscribe, getState, getState);

  useEffect(() => {
    syncOwner(owner);
  }, [owner]);

  // Until the effect runs for a new owner, don't expose the previous user's data.
  const stale = snapshot.owner !== owner;

  const isTracked = useCallback(
    (examId) =>
      !stale && snapshot.records.some((r) => r.exam_id === Number(examId)),
    [snapshot.records, stale]
  );

  const isPending = useCallback(
    (examId) => snapshot.pending.includes(Number(examId)),
    [snapshot.pending]
  );

  return {
    records: stale ? [] : snapshot.records,
    status: stale ? "loading" : snapshot.status,
    error: snapshot.error,
    isTracked,
    isPending,
    track: trackExam,
    untrack: untrackExam,
    refresh: loadRecords,
  };
}

/* ----------------------------------------------------------------------------
 * <TrackButton /> — drop into ExamDetails, SearchExams cards, etc.
 * ------------------------------------------------------------------------- */

export function TrackButton({ examId, className = "", size = "md" }) {
  const { status, isTracked, isPending, track, untrack } = useTrackedExams();
  const [feedback, setFeedback] = useState(null); // { ok, message }

  useEffect(() => {
    if (!feedback) return undefined;
    const timer = setTimeout(() => setFeedback(null), 3000);
    return () => clearTimeout(timer);
  }, [feedback]);

  const tracked = isTracked(examId);
  const busy = isPending(examId);
  const unavailable = status === "loading" || status === "idle";
  const Icon = tracked ? BookmarkCheck : Bookmark;

  async function handleClick(event) {
    // Safe to use inside clickable cards / links.
    event.preventDefault();
    event.stopPropagation();

    setFeedback(null);
    setFeedback(await (tracked ? untrack(examId) : track(examId)));
  }

  return (
    <div className={`inline-flex flex-col items-start gap-1.5 ${className}`}>
      <Button
        type="button"
        variant={tracked ? "secondary" : "primary"}
        loading={busy}
        disabled={unavailable || status === "error"}
        aria-pressed={tracked}
        onClick={handleClick}
        className={size === "sm" ? "!px-3 !py-1.5 !text-sm" : ""}
      >
        {!busy && <Icon size={size === "sm" ? 14 : 16} />}
        {tracked ? "Untrack exam" : "Track this exam"}
      </Button>

      {feedback && (
        <p
          role="status"
          className={`text-xs ${feedback.ok ? "text-signal-600" : "text-red-600"}`}
        >
          {feedback.message}
        </p>
      )}
    </div>
  );
}

/* ----------------------------------------------------------------------------
 * Page
 * ------------------------------------------------------------------------- */

function firstExamDate(notification) {
  const dates = notification?.exam_dates || [];
  if (dates.length === 0) return null;

  return (
    [...dates].sort(
      (a, b) => new Date(a.start_date).getTime() - new Date(b.start_date).getTime()
    )[0]?.start_date || null
  );
}

function TrackedExamRow({ record, exam, detailsLoading }) {
  const { isPending, untrack } = useTrackedExams();
  const [error, setError] = useState("");

  const notification = exam?.latest_approved_notification || null;
  const busy = isPending(record.exam_id);

  async function handleUntrack() {
    setError("");
    const result = await untrack(record.exam_id);
    if (!result.ok) setError(result.message);
  }

  return (
    <Card className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div className="min-w-0">
        <Link
          to={`/exams/${record.exam_id}`}
          className="block font-display font-semibold text-ink hover:text-gold"
        >
          {exam?.name || (detailsLoading ? "Loading exam…" : `Exam #${record.exam_id}`)}
        </Link>

        {exam && (
          <p className="mt-1 text-sm text-slate-500">
            {exam.conducting_body?.name || "—"} · {exam.type || "Exam"}
          </p>
        )}

        {exam && (
          <p className="mt-2 font-mono text-xs text-slate-500">
            Apply by {formatDate(notification?.application_end_date)} · Exam on{" "}
            {formatDate(firstExamDate(notification))}
          </p>
        )}

        {record.tracked_at && (
          <p className="mt-1 text-xs text-slate-400">
            Tracked {timeAgo(record.tracked_at)}
          </p>
        )}

        {error && (
          <p role="alert" className="mt-2 text-xs text-red-600">
            {error}
          </p>
        )}
      </div>

      <div className="flex shrink-0 items-center gap-2">
        <Link
          to={`/exams/${record.exam_id}`}
          className="rounded-xl px-4 py-2 text-center text-sm font-medium text-gold ring-1 ring-inset ring-indigo-100 transition hover:bg-indigo-50"
        >
          View details
        </Link>
        <Button
          type="button"
          variant="danger"
          loading={busy}
          onClick={handleUntrack}
          className="!px-4 !py-2 !text-sm"
        >
          Untrack
        </Button>
      </div>
    </Card>
  );
}

export default function TrackedExams() {
  const { records, status, error, refresh } = useTrackedExams();
  const [details, setDetails] = useState({}); // exam_id -> exam | null (failed)

  // Fetch full exam info for any tracked exam we haven't loaded yet.
  const missingKey = records
    .map((r) => r.exam_id)
    .filter((id) => !(id in details))
    .join(",");

  useEffect(() => {
    if (!missingKey) return undefined;

    let active = true;
    const ids = missingKey.split(",").map(Number);

    Promise.allSettled(ids.map((id) => getExamById(id))).then((results) => {
      if (!active) return;

      setDetails((prev) => {
        const next = { ...prev };
        results.forEach((result, index) => {
          next[ids[index]] = result.status === "fulfilled" ? result.value : null;
        });
        return next;
      });
    });

    return () => {
      active = false;
    };
  }, [missingKey]);

  const loading = status === "idle" || status === "loading";

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">
            Tracked exams
          </h1>
          <p className="mt-1.5 text-slate-600">
            The exams you're keeping an eye on. Updates to them show up in your
            notifications.
          </p>
        </div>

        {!loading && (
          <Button type="button" variant="secondary" onClick={refresh} className="!py-2 !text-sm">
            <RefreshCw size={14} /> Refresh
          </Button>
        )}
      </div>

      {loading && records.length === 0 && (
        <p className="text-sm text-slate-400">Loading your tracked exams...</p>
      )}

      {status === "error" && (
        <Card className="flex flex-col items-start gap-3" role="alert">
          <p className="text-sm text-red-600">{error}</p>
          <Button type="button" variant="secondary" onClick={refresh} className="!py-2 !text-sm">
            Try again
          </Button>
        </Card>
      )}

      {status === "ready" && records.length === 0 && (
        <Card>
          <p className="font-medium text-ink">You're not tracking any exams yet.</p>
          <p className="mt-1 text-sm text-slate-500">
            Open an exam and choose "Track this exam" to add it here.
          </p>
          <Link
            to="/search"
            className="mt-3 inline-block text-sm font-medium text-gold hover:underline"
          >
            Browse exams
          </Link>
        </Card>
      )}

      {records.length > 0 && (
        <div className="flex flex-col gap-3">
          {records.map((record) => (
            <TrackedExamRow
              key={record.tracking_id}
              record={record}
              exam={details[record.exam_id] || null}
              detailsLoading={!(record.exam_id in details)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
