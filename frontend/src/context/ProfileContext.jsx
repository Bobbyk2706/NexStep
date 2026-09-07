import { createContext, useCallback, useContext, useEffect, useState } from "react";
import * as profileApi from "../api/profile";
import * as examsApi from "../api/exams";
import { useAuth } from "./AuthContext";

const ProfileContext = createContext(null);

export function ProfileProvider({ children }) {
  const { user, hasProfile } = useAuth();
  const [profile, setProfile] = useState(null);
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    setLoading(true);
    const p = await profileApi.getProfile();
    setProfile(p);
    const e = await examsApi.getExams(p);
    setExams(e);
    setLoading(false);
  }, []);

  useEffect(() => {
    if (user && hasProfile) refresh();
    else setLoading(false);
  }, [user, hasProfile, refresh]);

  const eligibleExams = exams.filter((e) => e.eligible);

  return (
    <ProfileContext.Provider value={{ profile, exams, eligibleExams, loading, refresh }}>
      {children}
    </ProfileContext.Provider>
  );
}

export function useProfile() {
  const ctx = useContext(ProfileContext);
  if (!ctx) throw new Error("useProfile must be used within ProfileProvider");
  return ctx;
}
