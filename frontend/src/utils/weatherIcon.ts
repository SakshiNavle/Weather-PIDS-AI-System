import { Sun, Cloud, CloudRain, CloudLightning, CloudDrizzle, CloudFog, CloudSnow, CloudSun } from "lucide-react";
import type { ComponentType } from "react";

export function getWeatherIcon(condition: string | null | undefined): ComponentType<{ size?: number; strokeWidth?: number }> {
  const key = (condition || "").toLowerCase();
  if (key.includes("thunder")) return CloudLightning;
  if (key.includes("drizzle")) return CloudDrizzle;
  if (key.includes("rain")) return CloudRain;
  if (key.includes("snow")) return CloudSnow;
  if (key.includes("fog") || key.includes("mist") || key.includes("haze")) return CloudFog;
  if (key.includes("cloud")) return Cloud;
  if (key.includes("clear")) return Sun;
  return CloudSun;
}
