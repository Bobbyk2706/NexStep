import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export function RequireAuth() {
  const { user, checking } = useAuth();
  if (checking) return null;
  if (!user) return <Navigate to="/login" replace />;
  return <Outlet />;
}

export function RequireProfile() {
  const { hasProfile, checking } = useAuth();
  if (checking) return null;
  if (!hasProfile) return <Navigate to="/profile/setup" replace />;
  return <Outlet />;
}
