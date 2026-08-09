import { useCallback, useEffect, useRef, useState } from "react";

interface UsePollingOptions {
  intervalMs?: number;
  enabled?: boolean;
}

interface UsePollingResult<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
  lastUpdated: Date | null;
}

/**
 * Fetches data on mount and re-fetches on an interval, without a full
 * page reload. Tracks loading only on the *first* fetch so periodic
 * refreshes don't flash a skeleton over live data.
 */
export function usePolling<T>(
  fetcher: () => Promise<T>,
  options: UsePollingOptions = {}
): UsePollingResult<T> {
  const { intervalMs, enabled = true } = options;
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const hasLoadedOnce = useRef(false);
  const fetcherRef = useRef(fetcher);
  fetcherRef.current = fetcher;

  const load = useCallback(async () => {
    if (!hasLoadedOnce.current) setLoading(true);
    try {
      const result = await fetcherRef.current();
      setData(result);
      setError(null);
      setLastUpdated(new Date());
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Unable to reach the backend.";
      setError(message);
    } finally {
      hasLoadedOnce.current = true;
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!enabled) return;
    load();
    if (!intervalMs) return;
    const id = setInterval(load, intervalMs);
    return () => clearInterval(id);
  }, [enabled, intervalMs, load]);

  return { data, loading, error, refetch: load, lastUpdated };
}
