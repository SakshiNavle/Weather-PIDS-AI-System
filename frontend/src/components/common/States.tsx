import type { ReactNode } from "react";
import { Inbox, AlertOctagon, RefreshCw } from "lucide-react";
import "./states.css";

export function EmptyState({
  title,
  description,
  icon,
}: {
  title: string;
  description?: string;
  icon?: ReactNode;
}) {
  return (
    <div className="state-block state-block--empty">
      <div className="state-block__icon">{icon ?? <Inbox size={22} />}</div>
      <div className="state-block__title">{title}</div>
      {description && <div className="state-block__desc">{description}</div>}
    </div>
  );
}

export function ErrorState({
  title = "Unable to load data.",
  description,
  onRetry,
}: {
  title?: string;
  description?: string;
  onRetry?: () => void;
}) {
  return (
    <div className="state-block state-block--error">
      <div className="state-block__icon">
        <AlertOctagon size={22} />
      </div>
      <div className="state-block__title">{title}</div>
      {description && <div className="state-block__desc">{description}</div>}
      {onRetry && (
        <button className="retry-btn" onClick={onRetry}>
          <RefreshCw size={13} />
          Retry
        </button>
      )}
    </div>
  );
}

export function Skeleton({
  height = 16,
  width = "100%",
  radius = 6,
}: {
  height?: number | string;
  width?: number | string;
  radius?: number;
}) {
  return (
    <div
      className="skeleton"
      style={{ height, width, borderRadius: radius }}
      aria-hidden="true"
    />
  );
}

export function CardSkeleton({ lines = 3 }: { lines?: number }) {
  return (
    <div className="card-skeleton">
      <Skeleton height={12} width="40%" />
      <Skeleton height={26} width="60%" />
      {Array.from({ length: lines }).map((_, i) => (
        <Skeleton key={i} height={10} width={`${80 - i * 12}%`} />
      ))}
    </div>
  );
}
