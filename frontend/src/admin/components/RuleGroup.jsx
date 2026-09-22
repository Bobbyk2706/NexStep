function OperatorBadge({ op }) {
  const isAnd = op === "AND";
  return (
    <span
      className={`inline-flex items-center rounded-lg px-2.5 py-1 font-mono text-xs font-semibold tracking-wide ${
        isAnd ? "bg-indigo-700 text-white" : "bg-amber-500 text-white"
      }`}
    >
      {op}
    </span>
  );
}

function RuleRow({ rule }) {
  return (
    <div className="flex flex-wrap items-center gap-3 rounded-lg bg-slate-50 px-3 py-2 font-mono text-sm">
      <span className="font-medium text-ink">{rule.attribute}</span>
      <span className="rounded bg-surface px-1.5 py-0.5 text-xs text-gold ring-1 ring-inset ring-indigo-100">
        {rule.operator}
      </span>
      <span className="text-slate-600">{rule.value}</span>
    </div>
  );
}

export default function RuleGroup({ group, depth = 0 }) {
  if (!group) return null;
  const rules = group.rules || [];
  const childGroups = group.childGroups || [];

  return (
    <div className={`rounded-xl border ${depth === 0 ? "border-slate-200" : "border-slate-200/70"} bg-surface`}>
      <div className="flex items-center gap-2 border-b border-slate-100 px-4 py-2.5">
        <OperatorBadge op={group.logicalOperator} />
        <span className="text-xs text-slate-400">
          {rules.length} rule{rules.length === 1 ? "" : "s"}
          {childGroups.length > 0 ? `, ${childGroups.length} nested group${childGroups.length === 1 ? "" : "s"}` : ""}
        </span>
      </div>
      <div className="flex flex-col gap-2 p-4">
        {rules.map((rule, i) => (
          <RuleRow key={i} rule={rule} />
        ))}
        {rules.length === 0 && childGroups.length === 0 && (
          <p className="text-xs text-slate-400">No direct rules in this group.</p>
        )}
        {childGroups.length > 0 && (
          <div className="ml-1 flex flex-col gap-3 border-l-2 border-slate-200 pl-4">
            {childGroups.map((cg, i) => (
              <RuleGroup key={i} group={cg} depth={depth + 1} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
