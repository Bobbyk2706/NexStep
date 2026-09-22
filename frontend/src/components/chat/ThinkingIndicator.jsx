export default function ThinkingIndicator() {
  return (
    <div className="flex items-center gap-3 py-2">
      <span className="flex gap-1">
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className="h-1 w-1 rounded-full bg-gold/70"
            style={{ animation: "thinkPulse 1.4s ease-in-out infinite", animationDelay: `${i * 0.18}s` }}
          />
        ))}
      </span>
      <span className="font-mono text-[11px] uppercase tracking-wide text-slate-400">NexStep is thinking</span>
      <style>{`
        @keyframes thinkPulse { 0%, 80%, 100% { opacity: 0.25; } 40% { opacity: 1; } }
      `}</style>
    </div>
  );
}
