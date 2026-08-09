import { api } from "./axios";
import type { Recommendation } from "../types/recommendation";
import type { RiskLevel } from "../types/weather";

function normalizeRecommendations(response: unknown): Recommendation[] {
  if (Array.isArray(response)) {
    return response as Recommendation[];
  }

  if (response && typeof response === "object") {
    const obj = response as Record<string, unknown>;

    if (Array.isArray(obj.data)) {
      return obj.data as Recommendation[];
    }

    if (Array.isArray(obj.items)) {
      return obj.items as Recommendation[];
    }

    if (Array.isArray(obj.recommendations)) {
      return obj.recommendations as Recommendation[];
    }

    if (Array.isArray(obj.results)) {
      return obj.results as Recommendation[];
    }
  }

  return [];
}

export const recommendationApi = {
  list: async (): Promise<Recommendation[]> => {
    const response = await api.get("/recommendations");

    console.log("RECOMMENDATIONS RESPONSE:", response.data);

    return normalizeRecommendations(response.data);
  },

  byRisk: async (risk: RiskLevel): Promise<Recommendation[]> => {
    const response = await api.get(`/recommendations/risk/${risk}`);

    console.log(`RECOMMENDATIONS ${risk}:`, response.data);

    return normalizeRecommendations(response.data);
  },

  bySensor: async (sensorId: number | string): Promise<Recommendation[]> => {
    const response = await api.get(`/recommendations/sensor/${sensorId}`);

    return normalizeRecommendations(response.data);
  },
};

export default recommendationApi;