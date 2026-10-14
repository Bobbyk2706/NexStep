import { useState } from "react";
import { Plus, Trash2 } from "lucide-react";
import Card from "../../components/ui/Card";
import Button from "../../components/ui/Button";
import { SelectField, TextField, TextareaField } from "../../components/ui/Field";
import { dobBoundary } from "../utils/dob";

// What a rule may compare. Mirrors the backend (ATTRIBUTE_OPERATOR_RULES in
// eligibility_rule_validation.py): the server re-checks everything, this only
// keeps the choices valid.
const ATTRIBUTES = {
  "Date of Birth": {
    operators: ["<=", ">=", "<", ">", "=", "!="],
    input: "date",
    hint: "Born on/before (<=) or on/after (>=) this date",
  },
  "Educational Qualification": {
    operators: ["=", "!="],
    input: "select",
    options: ["10th", "12th / Senior Secondary", "Diploma", "Bachelor's", "Master's", "PhD"],
    hint: "A higher level also meets a lower requirement",
  },
  Nationality: { operators: ["=", "!="], input: "text", hint: "e.g. India" },
  State: { operators: ["=", "!="], input: "text", hint: "e.g. Kerala" },
  Specialization: { operators: ["=", "!="], input: "text", hint: "e.g. Computer Science" },
  Percentage: { operators: [">=", ">", "<=", "<", "=", "!="], input: "number", hint: "0 to 100" },
  CGPA: { operators: [">=", ">", "<=", "<", "=", "!="], input: "number", hint: "0 to 10" },
};

const MAX_DEPTH = 3;

function emptyRule() {
  return { attribute: "Nationality", operator: "=", value: "" };
}

function emptyGroup(operator = "AND") {
  return { logical_operator: operator, rules: [], child_groups: [] };
}

function cloneGroup(group) {
  return {
    logical_operator: group?.logical_operator || "AND",
    rules: (group?.rules || []).map((rule) => ({
      attribute: rule.attribute,
      operator: rule.operator,
      value: rule.value ?? "",
    })),
    child_groups: (group?.child_groups || []).map(cloneGroup),
  };
}

// The stored tree is a list of top-level groups that must all hold. The
// editor shows one root group: the single group itself, or an AND of several.
function initialRoot(ruleGroups) {
  const groups = ruleGroups || [];

  if (groups.length === 0) return emptyGroup("AND");
  if (groups.length === 1) return cloneGroup(groups[0]);

  return { logical_operator: "AND", rules: [], child_groups: groups.map(cloneGroup) };
}

// Drop blank rows and empty groups so a stray empty row does not block saving.
function prune(group) {
  const rules = group.rules.filter((rule) => String(rule.value).trim() !== "");
  const child_groups = group.child_groups.map(prune).filter((child) => child.rules.length > 0 || child.child_groups.length > 0);

  return { logical_operator: group.logical_operator, rules, child_groups };
}

function toInt(value) {
  const text = String(value ?? "").trim();
  if (text === "") return null;
  const number = Number(text);
  return Number.isInteger(number) ? number : null;
}

function RuleEditor({ rule, onChange, onRemove }) {
  // An attribute the editor does not list (e.g. from an older extraction) is
  // kept as it is rather than silently changed.
  const spec = ATTRIBUTES[rule.attribute] || { operators: ["=", "!="], input: "text", hint: "" };
  const attributeNames = Object.keys(ATTRIBUTES).includes(rule.attribute)
    ? Object.keys(ATTRIBUTES)
    : [rule.attribute, ...Object.keys(ATTRIBUTES)];

  function setAttribute(attribute) {
    const next = ATTRIBUTES[attribute];
    const operator = next.operators.includes(rule.operator) ? rule.operator : next.operators[0];
    onChange({ attribute, operator, value: next.input === "select" ? next.options[0] : "" });
  }

  let valueInput;

  if (spec.input === "select") {
    const options = !rule.value || spec.options.includes(rule.value) ? spec.options : [rule.value, ...spec.options];

    valueInput = (
      <SelectField value={rule.value} onChange={(e) => onChange({ ...rule, value: e.target.value })} aria-label="Value">
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </SelectField>
    );
  } else {
    valueInput = (
      <TextField
        type={spec.input === "date" ? "date" : spec.input === "number" ? "number" : "text"}
        step={spec.input === "number" ? "any" : undefined}
        value={rule.value}
        placeholder={spec.hint}
        onChange={(e) => onChange({ ...rule, value: e.target.value })}
        aria-label="Value"
      />
    );
  }

  return (
    <div className="grid items-start gap-2 sm:grid-cols-[1.4fr_0.6fr_1.6fr_auto]">
      <SelectField value={rule.attribute} onChange={(e) => setAttribute(e.target.value)} aria-label="Attribute">
        {attributeNames.map((name) => (
          <option key={name} value={name}>
            {name}
          </option>
        ))}
      </SelectField>

      <SelectField value={rule.operator} onChange={(e) => onChange({ ...rule, operator: e.target.value })} aria-label="Operator">
        {spec.operators.map((operator) => (
          <option key={operator} value={operator}>
            {operator}
          </option>
        ))}
      </SelectField>

      {valueInput}

      <button
        type="button"
        onClick={onRemove}
        className="mt-1.5 rounded-lg p-2 text-slate-400 hover:bg-slate-100 hover:text-amber-600"
        aria-label="Remove rule"
      >
        <Trash2 size={16} />
      </button>
    </div>
  );
}

function GroupEditor({ group, onChange, onRemove, depth }) {
  function setRule(index, rule) {
    const rules = group.rules.map((item, i) => (i === index ? rule : item));
    onChange({ ...group, rules });
  }

  function setChild(index, child) {
    const child_groups = group.child_groups.map((item, i) => (i === index ? child : item));
    onChange({ ...group, child_groups });
  }

  return (
    <div className={`rounded-xl border bg-surface ${depth === 0 ? "border-slate-200" : "border-slate-200/70"}`}>
      <div className="flex flex-wrap items-center gap-3 border-b border-slate-100 px-4 py-2.5">
        <select
          value={group.logical_operator}
          onChange={(e) => onChange({ ...group, logical_operator: e.target.value })}
          className="rounded-lg border border-slate-200 bg-slate-50 px-2 py-1 font-mono text-xs font-semibold"
          aria-label="Group operator"
        >
          <option value="AND">AND (all must be true)</option>
          <option value="OR">OR (any one is enough)</option>
        </select>

        {depth > 0 && (
          <button type="button" onClick={onRemove} className="ml-auto text-xs font-medium text-amber-600 hover:underline">
            Remove group
          </button>
        )}
      </div>

      <div className="flex flex-col gap-3 p-4">
        {group.rules.map((rule, index) => (
          <RuleEditor
            key={index}
            rule={rule}
            onChange={(next) => setRule(index, next)}
            onRemove={() => onChange({ ...group, rules: group.rules.filter((_, i) => i !== index) })}
          />
        ))}

        {group.child_groups.length > 0 && (
          <div className="ml-1 flex flex-col gap-3 border-l-2 border-slate-200 pl-4">
            {group.child_groups.map((child, index) => (
              <GroupEditor
                key={index}
                group={child}
                depth={depth + 1}
                onChange={(next) => setChild(index, next)}
                onRemove={() => onChange({ ...group, child_groups: group.child_groups.filter((_, i) => i !== index) })}
              />
            ))}
          </div>
        )}

        <div className="flex flex-wrap gap-2">
          <Button type="button" variant="secondary" onClick={() => onChange({ ...group, rules: [...group.rules, emptyRule()] })}>
            <Plus size={15} /> Add rule
          </Button>

          {depth < MAX_DEPTH && (
            <Button
              type="button"
              variant="ghost"
              onClick={() => onChange({ ...group, child_groups: [...group.child_groups, { ...emptyGroup("OR"), rules: [emptyRule()] }] })}
            >
              <Plus size={15} /> Add group
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}

// Lets an administrator enter or correct eligibility on a pending extraction.
// `initial` is extraction.eligibilityDraft; onSave receives the backend
// (ManualEligibility) payload.
export default function EligibilityEditor({ initial, notAvailable = false, saving = false, error = "", onSave, onCancel }) {
  const [minimumAge, setMinimumAge] = useState(initial?.minimum_age ?? "");
  const [maximumAge, setMaximumAge] = useState(initial?.maximum_age ?? "");
  const [qualification, setQualification] = useState(initial?.educational_qualification || "");
  const [nationality, setNationality] = useState(initial?.nationality || "");
  const [workExperience, setWorkExperience] = useState(initial?.work_experience || "");
  const [otherRequirements, setOtherRequirements] = useState((initial?.other_requirements || []).join("\n"));
  const [stated, setStated] = useState(!notAvailable);
  const [root, setRoot] = useState(() => initialRoot(initial?.rule_groups));
  const [localError, setLocalError] = useState("");

  // Age helper: turns "maximum 32, not attained, as on 2025-08-01" into the
  // date-of-birth rule the evaluator understands.
  const [helperKind, setHelperKind] = useState("maximum");
  const [helperYears, setHelperYears] = useState("");
  const [helperDate, setHelperDate] = useState("");
  const [helperExclusive, setHelperExclusive] = useState(false);

  function addAgeRule() {
    const boundary = dobBoundary(helperKind, helperYears, helperDate, helperExclusive);

    if (!boundary) {
      setLocalError("Enter the age in years and the date it is counted on.");
      return;
    }

    setLocalError("");
    setRoot((current) => ({
      ...current,
      rules: [...current.rules, { attribute: "Date of Birth", operator: boundary.operator, value: boundary.value }],
    }));

    // Keep the card in step with the rule it produced.
    if (helperKind === "minimum") setMinimumAge(toInt(helperYears) !== null ? String(toInt(helperYears) + (helperExclusive ? 1 : 0)) : minimumAge);
    else setMaximumAge(toInt(helperYears) !== null ? String(toInt(helperYears) - (helperExclusive ? 1 : 0)) : maximumAge);
  }

  function handleSave() {
    const pruned = prune(root);
    const hasRules = pruned.rules.length > 0 || pruned.child_groups.length > 0;

    if (stated && !hasRules) {
      setLocalError("Add at least one rule, or tick \"The notification does not state eligibility\".");
      return;
    }

    setLocalError("");

    onSave({
      minimum_age: toInt(minimumAge),
      maximum_age: toInt(maximumAge),
      educational_qualification: qualification.trim() || null,
      nationality: nationality.trim() || null,
      work_experience: workExperience.trim() || null,
      other_requirements: otherRequirements
        .split("\n")
        .map((line) => line.trim())
        .filter(Boolean),
      rule_groups: stated && hasRules ? [pruned] : [],
      not_available: !stated,
    });
  }

  const shownError = localError || error;

  return (
    <Card className="border-indigo-200">
      <h2 className="font-display text-base font-semibold text-ink">Enter eligibility</h2>
      <p className="mt-1 text-sm text-slate-500">
        Rules are checked the same way as extracted ones. Students are told whether they meet them, so enter only what the official
        notification says.
      </p>

      <div className="mt-5 grid gap-4 sm:grid-cols-2">
        <TextField id="el-min-age" label="Minimum age" type="number" min="0" max="120" value={minimumAge} onChange={(e) => setMinimumAge(e.target.value)} />
        <TextField id="el-max-age" label="Maximum age" type="number" min="0" max="120" value={maximumAge} onChange={(e) => setMaximumAge(e.target.value)} />
        <TextField id="el-qual" label="Educational qualification" value={qualification} onChange={(e) => setQualification(e.target.value)} placeholder="e.g. Bachelor's degree in any discipline" />
        <TextField id="el-nat" label="Nationality" value={nationality} onChange={(e) => setNationality(e.target.value)} placeholder="e.g. India, Nepal, Bhutan" />
        <TextField id="el-work" label="Work experience" value={workExperience} onChange={(e) => setWorkExperience(e.target.value)} />
        <TextareaField
          id="el-other"
          label="Other requirements"
          hint="One per line. Shown to students as written."
          value={otherRequirements}
          onChange={(e) => setOtherRequirements(e.target.value)}
        />
      </div>

      <label className="mt-5 flex items-start gap-2.5 text-sm text-ink">
        <input type="checkbox" className="mt-1" checked={!stated} onChange={(e) => setStated(!e.target.checked)} />
        <span>
          The notification does not state eligibility
          <span className="block text-xs text-slate-400">
            Students will see &ldquo;check the official notification&rdquo; instead of an eligible / not eligible result.
          </span>
        </span>
      </label>

      {stated && (
        <div className="mt-5 flex flex-col gap-4">
          <div className="rounded-xl bg-slate-50 p-4">
            <p className="text-sm font-medium text-ink">Add an age limit as a date-of-birth rule</p>
            <p className="mt-0.5 text-xs text-slate-400">
              The checker compares dates of birth, so an age is converted using the date it is counted on.
            </p>

            <div className="mt-3 grid items-end gap-3 sm:grid-cols-4">
              <SelectField id="el-h-kind" label="Limit" value={helperKind} onChange={(e) => setHelperKind(e.target.value)}>
                <option value="maximum">Maximum age</option>
                <option value="minimum">Minimum age</option>
              </SelectField>
              <TextField id="el-h-years" label="Years" type="number" min="0" max="120" value={helperYears} onChange={(e) => setHelperYears(e.target.value)} />
              <TextField id="el-h-date" label="Counted on" type="date" value={helperDate} onChange={(e) => setHelperDate(e.target.value)} />
              <Button type="button" variant="secondary" onClick={addAgeRule}>
                <Plus size={15} /> Add rule
              </Button>
            </div>

            <label className="mt-3 flex items-center gap-2 text-xs text-slate-500">
              <input type="checkbox" checked={helperExclusive} onChange={(e) => setHelperExclusive(e.target.checked)} />
              {helperKind === "maximum"
                ? "The notice says \"must not have attained / below\" this age (the limit itself is not allowed)"
                : "The notice says \"above / more than\" this age (the age itself is not allowed)"}
            </label>
          </div>

          <GroupEditor group={root} depth={0} onChange={setRoot} onRemove={() => {}} />
        </div>
      )}

      {shownError && <p className="mt-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{shownError}</p>}

      <div className="mt-5 flex justify-end gap-3">
        <Button type="button" variant="ghost" onClick={onCancel} disabled={saving}>
          Cancel
        </Button>
        <Button type="button" onClick={handleSave} loading={saving}>
          Save eligibility
        </Button>
      </div>
    </Card>
  );
}
