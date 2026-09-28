import { createContext, useContext, useEffect, useState } from "react";
import * as authApi from "../api/auth";
import * as profileApi from "../api/profile";
import { getToken, onSessionExpired } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [hasProfile, setHasProfile] = useState(false);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    // On reload, a real backend call would be GET /auth/me using the stored
    // token. Here we just check whether a profile was saved this session.
    async function restore() {
      try {
        const token = getToken();
        if (token) {
          const profile = await profileApi.getProfile();
          setUser({ name: profile?.name || "Student", email: "you@nexstep.app" });
          setHasProfile(Boolean(profile));
        }
      } catch {
        // Expired/invalid token: the client already cleared it. Fall through
        // so `checking` is released and the guards redirect to /login,
        // instead of hanging on a blank screen.
      } finally {
        setChecking(false);
      }
    }
    restore();
  }, []);

  // Any later request that comes back 401 logs the student out cleanly.
  useEffect(
    () =>
      onSessionExpired(() => {
        setUser(null);
        setHasProfile(false);
      }),
    []
  );

  async function login(credentials) {
    const res = await authApi.login(credentials);
    setUser(res.user);
    setHasProfile(res.hasProfile);
    return res;
  }

  async function signup(details) {
    const res = await authApi.signup(details);
    setUser(res.user);
    setHasProfile(res.hasProfile);
    return res;
  }

  function logout() {
    authApi.logout();
    setUser(null);
    setHasProfile(false);
  }

  function markProfileComplete() {
    setHasProfile(true);
  }

  return (
    <AuthContext.Provider
      value={{ user, hasProfile, checking, login, signup, logout, markProfileComplete }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}