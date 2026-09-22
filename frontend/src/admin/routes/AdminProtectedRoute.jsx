import { Navigate, Outlet } from "react-router-dom";
import { useAdminAuth } from "../context/AdminAuthContext";

export function RequireAdminAuth() {
  const { admin } = useAdminAuth();
  if (!admin) return <Navigate to="/login" replace />;
  return <Outlet />;
}
