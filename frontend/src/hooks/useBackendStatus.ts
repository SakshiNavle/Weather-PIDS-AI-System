import { useEffect, useState } from "react";
import { dashboardApi } from "../api/dashboardApi";

export type BackendStatus =
  | "checking"
  | "connected"
  | "offline";

export function useBackendStatus(
  intervalMs = 20000
): BackendStatus {
  const [status, setStatus] =
    useState<BackendStatus>("checking");

  useEffect(() => {
    let cancelled = false;

    const checkBackend = async () => {
      try {
        /*
         * /api/v1/dashboard already exists and is returning 200.
         * Therefore it is our backend availability check.
         */
        await dashboardApi.getDashboard();

        if (!cancelled) {
          setStatus("connected");
        }
      } catch {
        if (!cancelled) {
          setStatus("offline");
        }
      }
    };

    checkBackend();

    const intervalId = window.setInterval(
      checkBackend,
      intervalMs
    );

    return () => {
      cancelled = true;
      window.clearInterval(intervalId);
    };
  }, [intervalMs]);

  return status;
}