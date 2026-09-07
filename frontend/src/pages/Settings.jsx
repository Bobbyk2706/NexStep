import { Link, useNavigate } from "react-router-dom";
import { Pencil, LogOut } from "lucide-react";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import { useAuth } from "../context/AuthContext";
import { useProfile } from "../context/ProfileContext";

function Row({ label, value }) {
  return (
    <div className="flex items-center justify-between border-b border-slate-100 py-3 last:border-none">
      <span className="text-sm text-slate-500">{label}</span>
      <span className="text-sm font-medium text-ink">{value || "—"}</span>
    </div>
  );
}

export default function Settings() {
  const { user, logout } = useAuth();
  const { profile, loading } = useProfile();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/");
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="font-display text-2xl font-semibold tracking-tight text-ink md:text-3xl">Profile & settings</h1>
        <p className="mt-1.5 text-slate-600">Keep your academic details current — eligibility is re-checked automatically.</p>
      </div>

      <Card>
        <Row label="Name" value={user?.name} />
        <Row label="Email" value={user?.email} />
      </Card>

      {!loading && profile && (
        <Card>
          <div className="mb-2 flex items-center justify-between">
            <h2 className="font-display text-base font-semibold text-ink">Academic details</h2>
            <Link to="/profile/setup" className="flex items-center gap-1.5 text-sm font-medium text-indigo-700 hover:underline">
              <Pencil size={14} /> Edit
            </Link>
          </div>
          <Row label="College" value={profile.college} />
          <Row label="Branch" value={profile.branch} />
          <Row label="Year of study" value={profile.yearOfStudy} />
          <Row label="CGPA" value={profile.cgpa} />
          <Row label="Percentage" value={profile.percentage} />
          <Row label="State" value={profile.state} />
          <Row label="Nationality" value={profile.nationality} />
          {profile.hasHigherQualification && profile.previousQualification && (
            <Row
              label="Previous qualification"
              value={`${profile.previousQualification.level} · ${profile.previousQualification.institution || "—"}`}
            />
          )}
        </Card>
      )}

      {!loading && !profile && (
        <Card className="flex items-center justify-between">
          <p className="text-sm text-slate-500">You haven't built your profile yet.</p>
          <Link to="/profile/setup" className="text-sm font-medium text-indigo-700 hover:underline">
            Build profile
          </Link>
        </Card>
      )}

      <Button variant="danger" onClick={handleLogout} className="w-fit">
        <LogOut size={15} /> Log out
      </Button>
    </div>
  );
}
