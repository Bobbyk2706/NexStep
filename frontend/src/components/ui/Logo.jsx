export default function Logo({ className = "" }) {
  return (
    <span className={`font-display text-lg font-semibold tracking-tight text-ink ${className}`}>
      Nex<span className="text-gold">Step</span>
    </span>
  );
}
