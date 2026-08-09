export type RiskLevel = "LOW" | "MEDIUM" | "HIGH" | "SEVERE" | string;

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

  timestamp?: string | null;
  recorded_at?: string | null;
}

export interface WeatherCurrentResponse {
  location: string;
  weather: Weather;
}

export interface WeatherHistoryResponse {
  records: Weather[];
}

export type WeatherHistory = Weather[];