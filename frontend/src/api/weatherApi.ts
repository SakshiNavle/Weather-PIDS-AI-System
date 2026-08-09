import { api } from "./axios";
import type { Weather, WeatherHistory } from "../types/weather";

function normalizeWeather(item: unknown): Weather | null {
  if (!item || typeof item !== "object") {
    return null;
  }

  const obj = item as Record<string, unknown>;

  const timestamp =
    typeof obj.timestamp === "string"
      ? obj.timestamp
      : typeof obj.recorded_at === "string"
        ? obj.recorded_at
        : null;

  return {
    id: Number(obj.id ?? 0),

    site_name: String(
      obj.site_name ?? obj.location ?? "Unknown Site"
    ),

    temperature: Number(obj.temperature ?? 0),
    humidity: Number(obj.humidity ?? 0),
    wind_speed: Number(obj.wind_speed ?? 0),
    rainfall: Number(obj.rainfall ?? 0),

    weather_condition: String(
      obj.weather_condition ?? "Unknown"
    ),

    weather_description: String(
      obj.weather_description ?? ""
    ),

    storm: Boolean(obj.storm ?? false),

    weather_risk: String(
      obj.weather_risk ?? "LOW"
    ),

    timestamp,
    recorded_at: timestamp,
  };
}

function normalizeWeatherList(response: unknown): WeatherHistory {
  if (Array.isArray(response)) {
    return response
      .map(normalizeWeather)
      .filter((item): item is Weather => item !== null);
  }

  if (!response || typeof response !== "object") {
    return [];
  }

  const obj = response as Record<string, unknown>;

  // IMPORTANT:
  // Your backend returns { records: [...] }
  const records =
    Array.isArray(obj.records)
      ? obj.records
      : Array.isArray(obj.data)
        ? obj.data
        : Array.isArray(obj.items)
          ? obj.items
          : Array.isArray(obj.history)
            ? obj.history
            : Array.isArray(obj.results)
              ? obj.results
              : [];

  return records
    .map(normalizeWeather)
    .filter((item): item is Weather => item !== null);
}

export const weatherApi = {

  // GET /weather/current?city=Pune
  current: async (city: string): Promise<Weather | null> => {
    if (!city.trim()) {
      return null;
    }

    const response = await api.get("/weather/current", {
      params: {
        city: city.trim(),
      },
    });

    const data = response.data;

    if (!data) {
      return null;
    }

    /*
      Backend response:

      {
        "location": "Pune",
        "weather": {
          ...
        }
      }
    */

    if (
      typeof data === "object" &&
      data !== null &&
      !Array.isArray(data)
    ) {
      const obj = data as Record<string, unknown>;

      // Correct backend format: { location, weather }
      if (
        obj.weather &&
        typeof obj.weather === "object" &&
        !Array.isArray(obj.weather)
      ) {
        return normalizeWeather(obj.weather);
      }

      // Fallback
      return normalizeWeather(data);
    }

    if (Array.isArray(data)) {
      return normalizeWeather(data[0]);
    }

    return null;
  },

  // GET /weather/history?limit=72
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

  // POST /weather/refresh?city=Pune
  refresh: async (city: string): Promise<Weather | null> => {
    if (!city.trim()) {
      return null;
    }

    const response = await api.post(
      "/weather/refresh",
      null,
      {
        params: {
          city: city.trim(),
        },
      }
    );

    const data = response.data;

    if (
      data &&
      typeof data === "object" &&
      data.weather
    ) {
      return normalizeWeather(data.weather);
    }

    return normalizeWeather(data);
  },
};

export default weatherApi;