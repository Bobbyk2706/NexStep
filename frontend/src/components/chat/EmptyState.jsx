export default function EmptyState({ questions, onSelect }) {
  return (
    <div className="flex flex-1 flex-col items-center justify-center px-6 py-16 text-center">
      <p className="eyebrow mb-4">NexStep Assistant</p>
      <h1 className="max-w-md font-display text-[28px] leading-tight text-ink sm:text-[34px]">
        Ask about your exams, eligibility, or deadlines.
      </h1>
      <p className="mt-4 max-w-sm text-[14.5px] leading-relaxed text-slate-500">
        Answers are grounded in your saved profile and the exam database — not general guesses.
      </p>

      <div className="mt-10 grid w-full max-w-xl gap-2.5 sm:grid-cols-2">
        {questions.map((q) => (
          <button
            key={q}
            onClick={() => onSelect(q)}
            className="rounded-xl border border-slate-200 px-4 py-3 text-left text-[13.5px] text-slate-600 transition hover:border-indigo-200 hover:text-ink"
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  );
}
