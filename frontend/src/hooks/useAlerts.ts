import { alertApi } from "../api/alertApi";
import { usePolling } from "./usePolling";

export function useAlerts() {
  return usePolling(() => alertApi.list(), { intervalMs: 30000 });
}
