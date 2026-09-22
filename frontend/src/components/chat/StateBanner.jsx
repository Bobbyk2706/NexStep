import { SearchX, ServerOff, WifiOff } from "lucide-react";

const CONFIG = {
  "no-info": {
    icon: SearchX,
    title: "No matching information found",
    body: "I couldn't match this to a specific exam or feature. Try naming an exam directly (GATE, CAT, GRE, UPSC, NDA, CLAT), or ask how eligibility or deadlines work.",
    action: null,
  },
  "backend-unavailable": {
    icon: ServerOff,
    title: "NexStep Assistant is temporarily unavailable",
    body: "The reasoning service isn't responding right now. This is usually brief — try again in a moment.",
    action: "retry",
  },
  "network-error": {
    icon: WifiOff,
    title: "Connection lost",
    body: "Your message couldn't reach NexStep. Check your connection and try again.",
    action: "retry",
  },
};

export default function StateBanner({ kind, onRetry }) {
  const config = CONFIG[kind];
  if (!config) return null;
  const Icon = config.icon;

  return (
    <div className="flex items-start gap-4 border border-slate-200 bg-surface px-5 py-4">
      <Icon size={18} strokeWidth={1.5} className="mt-0.5 shrink-0 text-amber-600" />
      <div className="flex-1">
        <p className="text-[14px] font-medium text-ink">{config.title}</p>
        <p className="mt-1 text-[13px] leading-relaxed text-slate-500">{config.body}</p>
        {config.action === "retry" && onRetry && (
          <button onClick={onRetry} className="mt-3 border-b border-gold/50 text-[13px] text-ink hover:border-gold">
            Try again
          </button>
        )}
      </div>
    </div>
  );
}
