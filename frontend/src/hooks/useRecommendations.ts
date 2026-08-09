import { recommendationApi } from "../api/recommendationApi";
import { usePolling } from "./usePolling";

export function useRecommendations() {
  return usePolling(() => recommendationApi.list(), { intervalMs: 45000 });
}
