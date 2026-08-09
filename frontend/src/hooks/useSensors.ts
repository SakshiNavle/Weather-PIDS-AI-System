import { sensorApi } from "../api/sensorApi";
import { usePolling } from "./usePolling";

export function useSensors() {
  return usePolling(() => sensorApi.list(), { intervalMs: 60000 });
}
