import { weatherApi } from "../api/weatherApi";
import { usePolling } from "./usePolling";

export function useWeatherHistory(limit = 48) {
  return usePolling(
    () => weatherApi.history({ limit }),
    {
      intervalMs: 60000,
    }
  );
}