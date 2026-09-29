export function formatDate(dateStr) {
  if (!dateStr) return "Not available";

  const d = new Date(dateStr);
  if (isNaN(d)) return dateStr;

  return d.toLocaleDateString("en-IN", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

export function daysUntil(dateStr) {
  if (!dateStr) return null;

  const d = new Date(dateStr);
  if (isNaN(d)) return null;

  return Math.ceil((d - new Date()) / (1000 * 60 * 60 * 24));
}

export function timeAgo(dateStr) {
  if (!dateStr) return "";

  const diffMs = new Date() - new Date(dateStr);
  const mins = Math.floor(diffMs / 60000);

  if (mins < 60) return `${Math.max(0, mins)}m ago`;

  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;

  const days = Math.floor(hours / 24);
  if (days < 7) return `${days}d ago`;

  return formatDate(dateStr);
}
