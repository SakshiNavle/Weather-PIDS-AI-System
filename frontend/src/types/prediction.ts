import type { Sensitivity } from "./sensor";

export interface Prediction {
  id: number;
  sensor_id: number;
  sensor_name?: string;
  recommended_sensitivity: Sensitivity | string;
  confidence: number; // 0-1
  explanation?: string;
  created_at: string;
}

export interface RunAllResult {
  processed: number;
  successful: number;
  failed: number;
  failed_sensors?: { sensor_id: number; sensor_name?: string; reason?: string }[];
}
