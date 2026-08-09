export function formatTemperature(
  value: number | null | undefined
): string {
  if (
    value === null ||
    value === undefined ||
    !Number.isFinite(Number(value))
  ) {
    return "—";
  }

  return `${Number(value).toFixed(1)}°C`;
}

export function formatPercent(
  value: number | null | undefined
): string {
  if (
    value === null ||
    value === undefined ||
    !Number.isFinite(Number(value))
  ) {
    return "—";
  }

  return `${Math.round(Number(value))}%`;
}

export function formatConfidence(
  value: number | null | undefined
): string {
  if (
    value === null ||
    value === undefined ||
    !Number.isFinite(Number(value))
  ) {
    return "—";
  }

  const numericValue = Number(value);
  const pct = numericValue <= 1
    ? numericValue * 100
    : numericValue;

  return `${Math.round(pct)}%`;
}

export function confidenceToPercent(
  value: number | null | undefined
): number {
  if (
    value === null ||
    value === undefined ||
    !Number.isFinite(Number(value))
  ) {
    return 0;
  }

  const numericValue = Number(value);

  const pct = numericValue <= 1
    ? numericValue * 100
    : numericValue;

  return Math.max(0, Math.min(100, pct));
}

export function formatWindSpeed(
  value: number | null | undefined
): string {
  if (
    value === null ||
    value === undefined ||
    !Number.isFinite(Number(value))
  ) {
    return "—";
  }

  return `${Number(value).toFixed(1)} m/s`;
}

export function formatRainfall(
  value: number | null | undefined
): string {
  if (
    value === null ||
    value === undefined ||
    !Number.isFinite(Number(value))
  ) {
    return "—";
  }

  return `${Number(value).toFixed(2)} mm`;
}

export function formatDateTime(
  iso: string | null | undefined
): string {
  if (!iso) {
    return "—";
  }

  const d = new Date(iso);

  if (Number.isNaN(d.getTime())) {
    return "—";
  }

  const datePart = d.toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  });

  const timePart = d.toLocaleTimeString(undefined, {
    hour: "numeric",
    minute: "2-digit",
  });

  return `${datePart} · ${timePart}`;
}

export function formatRelativeTime(
  iso: string | null | undefined
): string {
  if (!iso) {
    return "—";
  }

  const d = new Date(iso);

  if (Number.isNaN(d.getTime())) {
    return "—";
  }

  const diffMs = Date.now() - d.getTime();

  // Future timestamp
  if (diffMs < 0) {
    return "just now";
  }

  const diffSec = Math.floor(diffMs / 1000);

  if (diffSec < 5) {
    return "just now";
  }

  if (diffSec < 60) {
    return `${diffSec}s ago`;
  }

  const diffMin = Math.floor(diffSec / 60);

  if (diffMin < 60) {
    return `${diffMin} min${diffMin === 1 ? "" : "s"} ago`;
  }

  const diffHr = Math.floor(diffMin / 60);

  if (diffHr < 24) {
    return `${diffHr} hr${diffHr === 1 ? "" : "s"} ago`;
  }

  const diffDay = Math.floor(diffHr / 24);

  return `${diffDay} day${diffDay === 1 ? "" : "s"} ago`;
}

export function titleCase(
  value: string | null | undefined
): string {
  if (!value) {
    return "—";
  }

  return value
    .toLowerCase()
    .split(/\s+/)
    .filter(Boolean)
    .map(
      (word) =>
        word.charAt(0).toUpperCase() +
        word.slice(1)
    )
    .join(" ");
}