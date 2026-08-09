import { useState } from "react";
import { Outlet } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { Header } from "./Header";
import { useBackendStatus } from "../../hooks/useBackendStatus";
import { useAlerts } from "../../hooks/useAlerts";
import "./shell.css";

export function AppShell() {
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const status = useBackendStatus();
  const { data: alerts, lastUpdated } = useAlerts();

  const activeAlertCount = (alerts ?? []).filter(
    (a) => (a.status || "").toUpperCase() === "ACTIVE"
  ).length;

  return (
    <div className="app-shell">
      <Sidebar
        collapsed={collapsed}
        onToggle={() => setCollapsed((c) => !c)}
        mobileOpen={mobileOpen}
        onCloseMobile={() => setMobileOpen(false)}
      />
      <div className="app-shell__main">
        <Header
          status={status}
          lastUpdated={lastUpdated}
          onMenuClick={() => setMobileOpen(true)}
          alertCount={activeAlertCount}
        />
        <main className="app-shell__content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
