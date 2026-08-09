import type { ReactNode } from "react";
import "./kpi-card.css";

interface KpiCardProps {
  label: string;
  value: ReactNode;
  icon: ReactNode;
  tone?: "neutral" | "accent" | "low" | "medium" | "high" | "severe";
  sub?: string;
}

export function KpiCard({ label, value, icon, tone = "neutral", sub }: KpiCardProps) {
  return (
    <div className={`kpi-card kpi-card--${tone}`}>
      <div className="kpi-card__icon">{icon}</div>
      <div className="kpi-card__body">
        <div className="kpi-card__value mono">{value}</div>
        <div className="kpi-card__label">{label}</div>
        {sub && <div className="kpi-card__sub">{sub}</div>}
      </div>
    </div>
  );
}
