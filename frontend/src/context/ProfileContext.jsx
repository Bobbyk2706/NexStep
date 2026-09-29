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
    if (!user || !hasProfile) {
      setProfile(null);
      setExams([]);
      setLoading(false);
      return;
    }

    setLoading(true);

    try {
      const currentProfile = await profileApi.getProfile();
      setProfile(currentProfile);

      if (currentProfile) {
        const currentExams = await examsApi.getExamsWithEligibility();
        setExams(currentExams || []);
      } else {
        setExams([]);
      }
    } finally {
      setLoading(false);
    }
  }, [user, hasProfile]);

  useEffect(() => {
    refresh().catch(() => {
      setProfile(null);
      setExams([]);
      setLoading(false);
    });
  }, [refresh]);

  const eligibleExams = exams.filter((exam) => exam.eligible);

  return (
    <ProfileContext.Provider
      value={{
        profile,
        exams,
        eligibleExams,
        loading,
        refresh,
      }}
    >
      {children}
    </ProfileContext.Provider>
  );
}

export function useProfile() {
  const ctx = useContext(ProfileContext);
  if (!ctx) throw new Error("useProfile must be used within ProfileProvider");
  return ctx;
}
