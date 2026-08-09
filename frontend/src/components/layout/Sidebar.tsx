import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Radio,
  CloudSun,
  BrainCircuit,
  ClipboardList,
  BellRing,
  Settings,
  ChevronsLeft,
  Radar,
} from "lucide-react";
import "./sidebar.css";

const NAV_ITEMS = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/sensors", label: "Sensors", icon: Radio },
  { to: "/weather", label: "Weather", icon: CloudSun },
  { to: "/predictions", label: "Predictions", icon: BrainCircuit },
  { to: "/recommendations", label: "Recommendations", icon: ClipboardList },
  { to: "/alerts", label: "Alerts", icon: BellRing },
  { to: "/settings", label: "Settings", icon: Settings },
];

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
  mobileOpen: boolean;
  onCloseMobile: () => void;
}

export function Sidebar({ collapsed, onToggle, mobileOpen, onCloseMobile }: SidebarProps) {
  return (
    <>
      {mobileOpen && <div className="sidebar-scrim" onClick={onCloseMobile} />}
      <aside className={`sidebar ${collapsed ? "sidebar--collapsed" : ""} ${mobileOpen ? "sidebar--mobile-open" : ""}`}>
        <div className="sidebar__brand">
          <div className="sidebar__brand-mark">
            <Radar size={18} />
          </div>
          {!collapsed && (
            <div className="sidebar__brand-text">
              <span className="sidebar__brand-name">PIDS</span>
              <span className="sidebar__brand-sub">Calibration AI</span>
            </div>
          )}
        </div>

        <nav className="sidebar__nav" aria-label="Primary">
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              onClick={onCloseMobile}
              className={({ isActive }) => `sidebar__link ${isActive ? "sidebar__link--active" : ""}`}
              title={collapsed ? label : undefined}
            >
              <Icon size={17} strokeWidth={2} />
              {!collapsed && <span>{label}</span>}
            </NavLink>
          ))}
        </nav>

        <button className="sidebar__collapse-btn" onClick={onToggle} aria-label="Toggle sidebar">
          <ChevronsLeft size={16} style={{ transform: collapsed ? "rotate(180deg)" : "none", transition: "transform 0.2s" }} />
          {!collapsed && <span>Collapse</span>}
        </button>
      </aside>
    </>
  );
}
