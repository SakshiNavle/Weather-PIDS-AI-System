import type { ReactElement } from "react";
import { AlertTriangle, ShieldCheck, ShieldAlert, Flame } from "lucide-react";
import "./badges.css";

interface RiskBadgeProps {
  risk: string | null | undefined;
  size?: "sm" | "md";
}

const RISK_CONFIG: Record<string, { icon: ReactElement; label: string; className: string }> = {
  LOW: { icon: <ShieldCheck size={12} />, label: "LOW", className: "risk-badge--low" },
  MEDIUM: { icon: <ShieldAlert size={12} />, label: "MEDIUM", className: "risk-badge--medium" },
  HIGH: { icon: <AlertTriangle size={12} />, label: "HIGH", className: "risk-badge--high" },
  SEVERE: { icon: <Flame size={12} />, label: "SEVERE", className: "risk-badge--severe" },
};

export function RiskBadge({ risk, size = "md" }: RiskBadgeProps) {
  const key = (risk || "").toUpperCase();
  const config = RISK_CONFIG[key] ?? {
    icon: <ShieldCheck size={12} />,
    label: key || "UNKNOWN",
    className: "risk-badge--unknown",
  };

  return (
    <span
      className={`risk-badge ${config.className} ${size === "sm" ? "risk-badge--sm" : ""}`}
    >
      {config.icon}
      {config.label}
    </span>
  );
}
