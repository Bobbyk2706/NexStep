const variants = {
  primary: "bg-indigo-700 text-white hover:bg-indigo-600 disabled:bg-indigo-300",
  secondary: "bg-white text-indigo-700 ring-1 ring-inset ring-indigo-100 hover:bg-indigo-50 disabled:text-slate-300",
  ghost: "text-slate-600 hover:bg-slate-50 disabled:text-slate-300",
  danger: "bg-white text-amber-600 ring-1 ring-inset ring-amber-200 hover:bg-amber-50",
};

export default function Button({
  variant = "primary",
  className = "",
  loading = false,
  children,
  disabled,
  ...props
}) {
  return (
    <button
      disabled={disabled || loading}
      className={`inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-[15px] font-medium transition disabled:cursor-not-allowed ${variants[variant]} ${className}`}
      {...props}
    >
      {loading && (
        <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-current border-t-transparent" />
      )}
      {children}
    </button>
  );
}
