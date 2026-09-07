export default function Card({ as: Tag = "div", className = "", children, ...props }) {
  return (
    <Tag
      className={`rounded-2xl border border-slate-200/70 bg-white p-5 shadow-card ${className}`}
      {...props}
    >
      {children}
    </Tag>
  );
}
