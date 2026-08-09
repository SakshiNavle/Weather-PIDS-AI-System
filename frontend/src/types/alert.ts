export type AlertStatus =
  | "ACTIVE"
  | "RESOLVED"
  | "INACTIVE";

export type RiskLevel =
  | "LOW"
  | "MEDIUM"
  | "HIGH"
  | "SEVERE";

export interface Alert {
  id: number;

  risk: RiskLevel | string;

  site_name?: string;

  message: string;

  status: AlertStatus | string;

  created_at: string;

  // Backend compatibility
  risk_level?: RiskLevel | string;
  is_active?: boolean;
}