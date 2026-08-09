import "./badges.css";

interface StatusBadgeProps {
  status: string | null | undefined;
}

export function StatusBadge({ status }: StatusBadgeProps) {
  const key = (status || "").toUpperCase();
  const isPositive = key === "ACTIVE";
  const isResolved = key === "RESOLVED";
  const className = isPositive
    ? "status-badge--active"
    : isResolved
    ? "status-badge--resolved"
    : "status-badge--inactive";

  return (
    <span className={`status-badge ${className}`}>
      <span className="status-badge__dot" />
      {key || "UNKNOWN"}
    </span>
  );
}
