import { predictionApi } from "../api/predictionApi";
import { usePolling } from "./usePolling";

export function usePredictions() {
  return usePolling(() => predictionApi.list(), { intervalMs: 60000 });
}
