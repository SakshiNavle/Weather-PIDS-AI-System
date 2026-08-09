import { api } from "./axios";
import type { Weather, WeatherHistory } from "../types/weather";

function normalizeWeatherList(response: unknown): WeatherHistory {
  if (Array.isArray(response)) {
    return response as Weather[];
  }

  if (response && typeof response === "object") {
    const obj = response as Record<string, unknown>;

    if (Array.isArray(obj.data)) {
      return obj.data as Weather[];
    }

    if (Array.isArray(obj.items)) {
      return obj.items as Weather[];
    }

    if (Array.isArray(obj.history)) {
      return obj.history as Weather[];
    }

    if (Array.isArray(obj.results)) {
      return obj.results as Weather[];
    }
  }

  return [];
}

export const weatherApi = {
  current: async (): Promise<Weather | null> => {
    const response = await api.get("/weather/current");
    const data = response.data;

    if (!data) {
      return null;
    }

    if (!Array.isArray(data) && typeof data === "object") {
      const obj = data as Record<string, unknown>;

      if (
        obj.data &&
        typeof obj.data === "object" &&
        !Array.isArray(obj.data)
      ) {
        return obj.data as Weather;
      }

      return data as Weather;
    }

    if (Array.isArray(data)) {
      return (data[0] as Weather) ?? null;
    }

    return null;
  },

  history: async (
    params?: {
      limit?: number;
      site_name?: string;
    }
  ): Promise<WeatherHistory> => {
    const response = await api.get("/weather/history", {
      params,
    });

    return normalizeWeatherList(response.data);
  },
};

export default weatherApi;