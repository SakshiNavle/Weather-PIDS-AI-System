import {
  Droplets,
  Wind,
  CloudRain,
  ShieldAlert,
  Zap,
  MapPin,
} from "lucide-react";

import type { Weather } from "../../types/weather";

import { RiskBadge } from "../common/RiskBadge";
import {
  CardSkeleton,
  EmptyState,
  ErrorState,
} from "../common/States";

import { getWeatherIcon } from "../../utils/weatherIcon";

import {
  formatTemperature,
  formatPercent,
  formatWindSpeed,
  formatRainfall,
  formatRelativeTime,
  titleCase,
} from "../../utils/format";

import "./weather-card.css";

interface WeatherCardProps {
  weather: Weather | null | undefined;
  loading?: boolean;
  error?: string | null;
  onRetry?: () => void;
}

export function WeatherCard({
  weather,
  loading,
  error,
  onRetry,
}: WeatherCardProps) {
  if (loading && !weather) {
    return (
      <div className="weather-card">
        <CardSkeleton lines={6} />
      </div>
    );
  }

  if (error && !weather) {
    return (
      <div className="weather-card">
        <ErrorState
          title="Unable to load weather."
          description={error}
          onRetry={onRetry}
        />
      </div>
    );
  }

  if (!weather) {
    return (
      <div className="weather-card">
        <EmptyState
          title="No weather data"
          description="Weather information is not available yet."
        />
      </div>
    );
  }

  const Icon = getWeatherIcon(
    weather.weather_condition
  );

  return (
    <div className="weather-card">
      <div className="weather-card__header">
        <div className="weather-card__location">
          <MapPin size={14} />

          <span>
            {weather.site_name}
          </span>
        </div>

        <RiskBadge
          risk={weather.weather_risk}
          size="sm"
        />
      </div>

      <div className="weather-card__condition">
        <div className="weather-card__icon">
          <Icon size={42} />
        </div>

        <div>
          <div className="weather-card__condition-name">
            {weather.weather_condition}
          </div>

          <div className="weather-card__description">
            {titleCase(
              weather.weather_description
            )}
          </div>
        </div>
      </div>

      <div className="weather-card__temp mono">
        {formatTemperature(
          weather.temperature
        )}
      </div>

      <div className="weather-card__grid">
        <div className="weather-card__stat">
          <Droplets size={14} />

          <span className="weather-card__stat-label">
            Humidity
          </span>

          <span className="weather-card__stat-value mono">
            {formatPercent(weather.humidity)}
          </span>
        </div>

        <div className="weather-card__stat">
          <Wind size={14} />

          <span className="weather-card__stat-label">
            Wind
          </span>

          <span className="weather-card__stat-value mono">
            {formatWindSpeed(
              weather.wind_speed
            )}
          </span>
        </div>

        <div className="weather-card__stat">
          <CloudRain size={14} />

          <span className="weather-card__stat-label">
            Rainfall
          </span>

          <span className="weather-card__stat-value mono">
            {formatRainfall(
              weather.rainfall
            )}
          </span>
        </div>

        <div className="weather-card__stat">
          <Zap size={14} />

          <span className="weather-card__stat-label">
            Storm
          </span>

          <span className="weather-card__stat-value mono">
            {weather.storm ? "Yes" : "No"}
          </span>
        </div>
      </div>

      <div className="weather-card__footer">
        <div className="weather-card__risk">
          <ShieldAlert size={13} />

          <span>Risk</span>

          <RiskBadge
            risk={weather.weather_risk}
            size="sm"
          />
        </div>

        <div className="weather-card__updated">
          Updated{" "}
          {formatRelativeTime(
            weather.recorded_at
          )}
        </div>
      </div>
    </div>
  );
}