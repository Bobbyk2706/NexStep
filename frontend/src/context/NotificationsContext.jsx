import { createContext, useCallback, useContext, useEffect, useState } from "react";
import * as notificationsApi from "../api/notifications";
import { useAuth } from "./AuthContext";

const NotificationsContext = createContext(null);

export function NotificationsProvider({ children }) {
  const { user } = useAuth();
  const [notifications, setNotifications] = useState([]);

  const refresh = useCallback(async () => {
    const data = await notificationsApi.getNotifications();
    setNotifications(data);
  }, []);

  useEffect(() => {
    if (user) refresh();
  }, [user, refresh]);

  async function markRead(id) {
    const updated = await notificationsApi.markAsRead(id);
    setNotifications(updated);
  }

  async function markAllRead() {
    const updated = await notificationsApi.markAllAsRead();
    setNotifications(updated);
  }

  const unreadCount = notifications.filter((n) => !n.read).length;

  return (
    <NotificationsContext.Provider value={{ notifications, unreadCount, refresh, markRead, markAllRead }}>
      {children}
    </NotificationsContext.Provider>
  );
}

export function useNotifications() {
  const ctx = useContext(NotificationsContext);
  if (!ctx) throw new Error("useNotifications must be used within NotificationsProvider");
  return ctx;
}
