export type SensorStatus =
  | "ACTIVE"
  | "INACTIVE";

export type Sensitivity =
  | "LOW"
  | "MEDIUM"
  | "HIGH";

export interface Sensor {
  id: number;

  // Frontend name
  name: string;

  sensor_type: string;

  location: string;

  status: SensorStatus | string;

  sensitivity: Sensitivity | string;

  created_at?: string;

  updated_at?: string;

  last_prediction_at?: string;

  // Backend compatibility
  sensor_name?: string;

  current_sensitivity?: Sensitivity | string;
}

export interface SensorCreatePayload {
  name: string;

  sensor_type: string;

  location: string;

  sensitivity: Sensitivity;

  status?: SensorStatus;
}

export type SensorUpdatePayload =
  Partial<SensorCreatePayload>;