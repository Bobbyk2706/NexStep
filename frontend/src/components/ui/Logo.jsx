export default function Logo({ className = "" }) {
  return (
    <span className={`font-display text-lg font-semibold tracking-tight text-ink ${className}`}>
      Nex<span className="text-indigo-700">Step</span>
    </span>
  );
}
