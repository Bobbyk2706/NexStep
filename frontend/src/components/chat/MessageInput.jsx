import { useEffect, useRef, useState } from "react";
import { ArrowUp } from "lucide-react";

export default function MessageInput({ onSend, disabled }) {
  const [value, setValue] = useState("");
  const ref = useRef(null);

  useEffect(() => {
    if (ref.current) {
      ref.current.style.height = "auto";
      ref.current.style.height = `${Math.min(ref.current.scrollHeight, 160)}px`;
    }
  }, [value]);

  function handleSubmit(e) {
    e.preventDefault();
    if (!value.trim() || disabled) return;
    onSend(value.trim());
    setValue("");
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) handleSubmit(e);
  }

  return (
    <form onSubmit={handleSubmit} className="border border-slate-200 bg-surface transition focus-within:border-gold/50">
      <textarea
        ref={ref}
        rows={1}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask about GATE, CAT, deadlines, or your eligibility..."
        aria-label="Ask NexStep a question"
        disabled={disabled}
        className="w-full resize-none bg-transparent px-5 pb-2 pt-4 text-[15px] leading-relaxed text-ink placeholder:text-slate-400 focus:outline-none disabled:opacity-50"
      />
      <div className="flex items-center justify-between px-5 pb-3.5 pt-1">
        <span className="font-mono text-[10.5px] text-slate-400">
          <kbd className="rounded border border-slate-200 px-1.5 py-0.5">Enter</kbd> to send ·{" "}
          <kbd className="rounded border border-slate-200 px-1.5 py-0.5">Shift+Enter</kbd> for new line
        </span>
        <button
          type="submit"
          disabled={!value.trim() || disabled}
          aria-label="Send"
          className="flex h-8 w-8 items-center justify-center rounded-full bg-indigo-700 text-white transition hover:bg-indigo-600 disabled:opacity-30"
        >
          <ArrowUp size={15} strokeWidth={2} />
        </button>
      </div>
    </form>
  );
}
