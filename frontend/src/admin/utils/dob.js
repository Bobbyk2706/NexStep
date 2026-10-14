// Age limit -> date-of-birth rule, with the same arithmetic as the backend
// (backend/app/ai/extraction/age_rules.py), so a rule typed in here means
// exactly what an AI-extracted one means.
//
//   maximum, "up to N"            age <= N  -> born on or after (ref - (N+1) years) + 1 day
//   maximum, "below N" (exclusive) age <  N  -> born on or after (ref - N years) + 1 day
//   minimum, "at least N"         age >= N  -> born on or before (ref - N years)
//   minimum, "above N" (exclusive) age >  N  -> born on or before (ref - (N+1) years)

function parseIso(iso) {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || "");
  if (!match) return null;
  return { year: Number(match[1]), month: Number(match[2]), day: Number(match[3]) };
}

function toIso(date) {
  const y = String(date.getUTCFullYear()).padStart(4, "0");
  const m = String(date.getUTCMonth() + 1).padStart(2, "0");
  const d = String(date.getUTCDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

function subtractYears({ year, month, day }, years) {
  const date = new Date(Date.UTC(year - years, month - 1, day));

  // 29 February in a year that has none rolls into March; use the 28th.
  if (date.getUTCMonth() !== month - 1) {
    return new Date(Date.UTC(year - years, month - 1, 28));
  }

  return date;
}

export function dobBoundary(kind, years, referenceIso, exclusive = false) {
  const reference = parseIso(referenceIso);
  const n = Number(years);

  if (!reference || !Number.isInteger(n) || n < 0 || n > 120) {
    return null;
  }

  if (kind === "maximum") {
    const effective = exclusive ? n - 1 : n;
    const date = subtractYears(reference, effective + 1);
    date.setUTCDate(date.getUTCDate() + 1);
    return { operator: ">=", value: toIso(date) };
  }

  const effective = exclusive ? n + 1 : n;
  return { operator: "<=", value: toIso(subtractYears(reference, effective)) };
}
