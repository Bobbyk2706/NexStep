import { createContext, useContext, useEffect, useState } from "react";
import * as adminAuthApi from "../api/adminAuth";
import { getAdminToken, onAdminSessionExpired } from "../api/adminClient";

const AdminAuthContext = createContext(null);

export function AdminAuthProvider({ children }) {
  const [admin, setAdmin] = useState(null);
  // Only "checking" if there's a stored token to validate.
  const [checking, setChecking] = useState(() => Boolean(getAdminToken()));

  // A token sitting in localStorage proves nothing — ask the backend.
  useEffect(() => {
    let cancelled = false;
    if (!getAdminToken()) {
      setChecking(false);
      return;
    }
    adminAuthApi
      .fetchAdminSession()
      .then((a) => {
        if (!cancelled) setAdmin(a);
      })
      .catch(() => {
        // 401s already cleared the session inside the client; anything else
        // (e.g. backend down) leaves admin null, so the guard sends them to
        // /login instead of showing a dashboard we can't back with data.
      })
      .finally(() => {
        if (!cancelled) setChecking(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  // Any later API call that comes back 401 (after a failed refresh) lands here.
  useEffect(() => onAdminSessionExpired(() => setAdmin(null)), []);

  async function login(credentials) {
    const res = await adminAuthApi.adminLogin(credentials);
    setAdmin(res.admin);
    return res;
  }

  function logout() {
    adminAuthApi.adminLogout();
    setAdmin(null);
  }

  return (
    <AdminAuthContext.Provider value={{ admin, checking, login, logout }}>
      {children}
    </AdminAuthContext.Provider>
  );
}

export function useAdminAuth() {
  const ctx = useContext(AdminAuthContext);
  if (!ctx) throw new Error("useAdminAuth must be used within AdminAuthProvider");
  return ctx;
}