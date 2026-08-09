import { useCallback, useEffect, useState } from "react";
import weatherApi from "../api/weatherApi";

export function useCurrentWeather(city: string) {
  const [data, setData] = useState<Awaited<ReturnType<typeof weatherApi.current>> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchWeather = useCallback(async () => {
    if (!city.trim()) {
      setData(null);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await weatherApi.current(city.trim());

      setData(response);
    } catch (err: any) {
      console.error("Weather error:", err);

      const message =
        err?.response?.data?.detail ||
        err?.message ||
        "Unable to fetch weather.";

      setError(
        Array.isArray(message)
          ? message.map((x) => x.msg).join(", ")
          : String(message)
      );
    } finally {
      setLoading(false);
    }
  }, [city]);

  return {
    data,
    loading,
    error,
    refetch: fetchWeather,
  };
}


export function useWeatherHistory(limit = 72) {
  const [data, setData] = useState<Awaited<ReturnType<typeof weatherApi.history>>>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchHistory = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const records = await weatherApi.history({ limit });

      setData(Array.isArray(records) ? records : []);
    } catch (err: any) {
      console.error("Weather history error:", err);

      setError(
        err?.response?.data?.detail ||
          err?.message ||
          "Unable to load weather history."
      );

      setData([]);
    } finally {
      setLoading(false);
    }
  }, [limit]);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  return {
    data,
    loading,
    error,
    refetch: fetchHistory,
  };
}