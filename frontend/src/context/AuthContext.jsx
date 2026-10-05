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
    let mounted = true;

    async function restoreSession() {
      try {
        if (!getToken()) return;

        const [currentUser, profile] = await Promise.all([
          authApi.getCurrentUser(),
          profileApi.getProfile(),
        ]);

        if (!mounted) return;

        setUser(currentUser);
        setHasProfile(Boolean(profile));
      } catch {
        if (!mounted) return;
        setUser(null);
        setHasProfile(false);
      } finally {
        if (mounted) setChecking(false);
      }
    }

    restoreSession();

    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    return onSessionExpired(() => {
      setUser(null);
      setHasProfile(false);
    });
  }, []);

  async function login(credentials) {
    const res = await authApi.login(credentials);
    setUser(res.user || null);
    setHasProfile(Boolean(res.hasProfile));
    return res;
  }

  // Signup step 1: emails a code. No account or session exists yet.
  async function startSignup(details) {
    return authApi.startSignup(details);
  }

  // Signup step 2: confirms the code, creates the account, signs the person in.
  async function verifySignup(email, code) {
    const res = await authApi.verifySignup({ email, code });
    setUser(res.user || null);
    setHasProfile(Boolean(res.hasProfile));
    return res;
  }

  async function resendSignupCode(email) {
    return authApi.resendSignupCode(email);
  }

  async function logout() {
    try {
      await authApi.logout();
    } finally {
      setUser(null);
      setHasProfile(false);
    }
  }

  function markProfileComplete() {
    setHasProfile(true);
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        hasProfile,
        checking,
        login,
        startSignup,
        verifySignup,
        resendSignupCode,
        logout,
        markProfileComplete,
      }}
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