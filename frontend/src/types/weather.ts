export type RiskLevel =
  | "LOW"
  | "MEDIUM"
  | "HIGH"
  | "SEVERE"
  | string;

export interface Weather {
  id: number;

  site_name: string;

  temperature: number;
  humidity: number;
  wind_speed: number;
  rainfall: number;

  weather_condition: string;
  weather_description: string;

  storm: boolean;

  weather_risk: RiskLevel;

  /*
   * Some backend responses use timestamp,
   * while database records may expose recorded_at.
   */
  timestamp?: string | null;
  recorded_at?: string | null;
}

export type WeatherHistory = Weather[];