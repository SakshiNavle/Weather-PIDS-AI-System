import type { Sensitivity } from "./sensor";

export type RecommendationRisk =
  | "LOW"
  | "MEDIUM"
  | "HIGH"
  | "SEVERE"
  | string;

export interface Recommendation {
  id: number;
  sensor_id: number;

  risk_level: RecommendationRisk;

  title: string;
  description: string;

  action?: string | null;

  recommended_sensitivity?: Sensitivity | string | null;

  created_at: string;
}