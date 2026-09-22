<<<<<<< HEAD
export default function Card({ as: Tag = "div", elevated = false, className = "", children, ...props }) {
  return (
    <Tag
      className={`rounded-2xl border border-slate-200/70 bg-surface p-5 ${elevated ? "shadow-soft" : ""} ${className}`}
=======
export default function Card({ as: Tag = "div", className = "", children, ...props }) {
  return (
    <Tag
      className={`rounded-2xl border border-slate-200/70 bg-white p-5 shadow-card ${className}`}
>>>>>>> origin/main
      {...props}
    >
      {children}
    </Tag>
  );
}
