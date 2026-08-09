import { dashboardApi } from "../api/dashboardApi";
import { usePolling } from "./usePolling";

export function useDashboard() {
  return usePolling(() => dashboardApi.getDashboard(), { intervalMs: 30000 });
}
