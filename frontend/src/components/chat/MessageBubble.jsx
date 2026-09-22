import { useState } from "react";
import { Copy, RotateCcw, ThumbsUp, ThumbsDown, Check } from "lucide-react";
import SourcesPanel from "./SourcesPanel";
import ThinkingIndicator from "./ThinkingIndicator";
import StateBanner from "./StateBanner";

function ActionButton({ icon: Icon, label, onClick, active }) {
  return (
    <button
      onClick={onClick}
      aria-label={label}
      className={`rounded p-1.5 transition ${active ? "text-gold" : "text-slate-400 hover:text-ink"}`}
    >
      <Icon size={15} strokeWidth={1.5} />
    </button>
  );
}

export default function MessageBubble({ message, onRetry, onRegenerate }) {
  const [copied, setCopied] = useState(false);
  const [feedback, setFeedback] = useState(null);

  if (message.role === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[75%] rounded-md bg-indigo-50 px-4 py-2.5 text-[15px] leading-relaxed text-ink sm:max-w-[65%]">
          {message.content}
        </div>
      </div>
    );
  }

  if (message.status === "thinking") return <ThinkingIndicator />;
  if (["no-info", "backend-unavailable", "network-error"].includes(message.status)) {
    return <StateBanner kind={message.status} onRetry={onRetry} />;
  }

  function handleCopy() {
    navigator.clipboard?.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 1600);
  }

  return (
    <div className="group max-w-2xl">
      <p className="text-[15.5px] leading-[1.75] text-ink">{message.content}</p>
      <SourcesPanel sources={message.sources} />
      <div className="mt-3 flex items-center gap-1 opacity-60 transition group-hover:opacity-100">
        <ActionButton icon={copied ? Check : Copy} label="Copy answer" onClick={handleCopy} active={copied} />
        <ActionButton icon={RotateCcw} label="Regenerate" onClick={() => onRegenerate?.(message.id)} />
        <span className="mx-1 h-3 w-px bg-slate-200" />
        <ActionButton icon={ThumbsUp} label="Good answer" onClick={() => setFeedback("up")} active={feedback === "up"} />
        <ActionButton icon={ThumbsDown} label="Poor answer" onClick={() => setFeedback("down")} active={feedback === "down"} />
      </div>
    </div>
  );
}
