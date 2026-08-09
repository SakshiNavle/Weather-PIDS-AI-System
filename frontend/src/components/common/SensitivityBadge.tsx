import "./badges.css";

interface SensitivityBadgeProps {
  value: string | null | undefined;
}

export function SensitivityBadge({ value }: SensitivityBadgeProps) {
  const key = (value || "").toUpperCase();
  const className =
    key === "HIGH"
      ? "sens-badge--high"
      : key === "MEDIUM"
      ? "sens-badge--medium"
      : key === "LOW"
      ? "sens-badge--low"
      : "sens-badge--unknown";

  return <span className={`sens-badge ${className}`}>{key || "—"}</span>;
}
