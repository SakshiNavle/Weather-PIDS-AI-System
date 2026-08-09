import type { Weather } from "./weather";
import type { Recommendation } from "./recommendation";
import type { Alert } from "./alert";

export interface DashboardData {
  total_sensors: number;
  active_sensors: number;
  inactive_sensors: number;

  total_alerts: number;
  active_alerts: number;

  latest_weather: Weather | null;

  recommendations: Recommendation[];

  recent_alerts: Alert[];
}