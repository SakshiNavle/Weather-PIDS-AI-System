import { api } from "./axios";
import type { Recommendation } from "../types/recommendation";
import type { RiskLevel } from "../types/weather";

export const recommendationApi = {
  list: () => api.get<Recommendation[]>("/recommendations").then((r) => r.data),
  byRisk: (risk: RiskLevel) =>
    api.get<Recommendation[]>(`/recommendations/risk/${risk}`).then((r) => r.data),
  bySensor: (sensorId: number | string) =>
    api.get<Recommendation[]>(`/recommendations/sensor/${sensorId}`).then((r) => r.data),
};
