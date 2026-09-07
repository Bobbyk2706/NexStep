const baseInput =
  "w-full rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 text-[15px] text-ink placeholder:text-slate-400 transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 disabled:bg-slate-50 disabled:text-slate-400";

function Wrapper({ label, htmlFor, error, hint, required, children }) {
  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label htmlFor={htmlFor} className="text-sm font-medium text-ink">
          {label} {required && <span className="text-amber-500">*</span>}
        </label>
      )}
      {children}
      {hint && !error && <p className="text-xs text-slate-400">{hint}</p>}
      {error && <p className="text-xs text-amber-600">{error}</p>}
    </div>
  );
}

export function TextField({ label, id, error, hint, required, className = "", ...props }) {
  return (
    <Wrapper label={label} htmlFor={id} error={error} hint={hint} required={required}>
      <input id={id} className={`${baseInput} ${className}`} {...props} />
    </Wrapper>
  );
}

export function SelectField({ label, id, error, hint, required, children, className = "", ...props }) {
  return (
    <Wrapper label={label} htmlFor={id} error={error} hint={hint} required={required}>
      <select id={id} className={`${baseInput} ${className}`} {...props}>
        {children}
      </select>
    </Wrapper>
  );
}

export function TextareaField({ label, id, error, hint, required, className = "", ...props }) {
  return (
    <Wrapper label={label} htmlFor={id} error={error} hint={hint} required={required}>
      <textarea id={id} className={`${baseInput} min-h-[90px] resize-y ${className}`} {...props} />
    </Wrapper>
  );
}
