import type { RiskLevel } from "./weather";
import type { Sensitivity } from "./sensor";

export interface Recommendation {
  id: number;
  sensor_id: number;
  sensor_name?: string;
  risk: RiskLevel | string;
  recommended_sensitivity: Sensitivity | string;
  message: string;
  action?: string;
  created_at: string;
}
