import { createContext, useContext, useState } from "react";
import * as adminAuthApi from "../api/adminAuth";
import { getAdminToken } from "../api/adminAuth";

const AdminAuthContext = createContext(null);

export function AdminAuthProvider({ children }) {
  const [admin, setAdmin] = useState(() => {
    const token = getAdminToken();
    return token ? { name: "Admin", email: "" } : null;
  });

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
    <AdminAuthContext.Provider value={{ admin, login, logout }}>
      {children}
    </AdminAuthContext.Provider>
  );
}

export function useAdminAuth() {
  const ctx = useContext(AdminAuthContext);
  if (!ctx) throw new Error("useAdminAuth must be used within AdminAuthProvider");
  return ctx;
}
