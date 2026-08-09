import { Bell, Menu, UserCircle } from "lucide-react";
import type { BackendStatus } from "../../hooks/useBackendStatus";
import { formatRelativeTime } from "../../utils/format";
import "./header.css";

interface HeaderProps {
  status: BackendStatus;
  lastUpdated: Date | null;
  onMenuClick: () => void;
  alertCount: number;
}

export function Header({ status, lastUpdated, onMenuClick, alertCount }: HeaderProps) {
  const statusLabel =
    status === "connected" ? "Backend Connected" : status === "offline" ? "Backend Offline" : "Checking Connection";

  return (
    <header className="app-header">
      <button className="app-header__menu-btn" onClick={onMenuClick} aria-label="Open navigation">
        <Menu size={19} />
      </button>

      <div className={`connection-pill connection-pill--${status}`}>
        <span className="connection-pill__dot" />
        {statusLabel}
      </div>

      <div className="app-header__spacer" />

      <div className="app-header__updated">
        Last updated {lastUpdated ? formatRelativeTime(lastUpdated.toISOString()) : "—"}
      </div>

      <button className="app-header__icon-btn" aria-label="Notifications">
        <Bell size={17} />
        {alertCount > 0 && <span className="app-header__badge">{alertCount > 9 ? "9+" : alertCount}</span>}
      </button>

      <div className="app-header__user">
        <UserCircle size={26} />
        <span className="app-header__user-name">Operator</span>
      </div>
    </header>
  );
}
