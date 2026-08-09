import {
  Radio,
  CheckCircle2,
  PowerOff,
  BellRing,
  Gauge,
} from "lucide-react";

import { useDashboard } from "../hooks/useDashboard";
import { useWeatherHistory } from "../hooks/useWeather";

import { KpiCard } from "../components/dashboard/KpiCard";
import { RiskGauge } from "../components/dashboard/RiskGauge";
import { ChartCard } from "../components/weather/ChartCard";
import { RecommendationCard } from "../components/recommendations/RecommendationCard";
import { AlertRow } from "../components/alerts/AlertRow";
import { SensitivityBadge } from "../components/common/SensitivityBadge";

function WeatherCard({
  weather,
  loading,
  error,
  onRetry,
}: {
  weather?: any;
  loading?: boolean;
  error?: string | null;
  onRetry?: () => void;
}) {
  if (loading) {
    return (
      <div className="panel">
        <div className="panel__header">
          <h3>Current Weather</h3>
        </div>
        <div className="state state--loading">
          Loading weather data...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="panel">
        <div className="panel__header">
          <h3>Current Weather</h3>
        </div>
        <div className="state state--error">
          {error}
          {onRetry ? (
            <button
              type="button"
              onClick={onRetry}
              className="button button--ghost"
            >
              Retry
            </button>
          ) : null}
        </div>
      </div>
    );
  }

  const latest = weather ?? {};

  return (
    <div className="panel weather-card">
      <div className="panel__header">
        <h3>Current Weather</h3>
        <span className="panel__header-sub">
          {latest.site_name ?? "Site"}
        </span>
      </div>

      <div className="weather-card__grid">
        <div>
          <div className="weather-card__temp">
            {latest.temperature ?? "—"}°C
          </div>
          <div className="weather-card__condition">
            {latest.weather_description ??
              latest.weather_condition ??
              "No data"}
          </div>
        </div>

        <div className="weather-card__stats">
          <div>Humidity: {latest.humidity ?? "—"}%</div>
          <div>Wind: {latest.wind_speed ?? "—"} m/s</div>
          <div>Rainfall: {latest.rainfall ?? "—"} mm</div>
          <div>Risk: {latest.weather_risk ?? "—"}</div>
        </div>
      </div>
    </div>
  );
}

import {
  EmptyState,
  ErrorState,
  CardSkeleton,
} from "../components/common/States";

import { formatDateTime } from "../utils/format";

export default function Dashboard() {
  const {
    data,
    loading,
    error,
    refetch,
  } = useDashboard();

  const {
    data: history,
    loading: historyLoading,
    error: historyError,
    refetch: refetchHistory,
  } = useWeatherHistory(48);

  /*
   * IMPORTANT:
   * Never assume history is an array.
   *
   * weatherApi.ts already normalizes it,
   * but this extra check guarantees Dashboard
   * cannot crash because of .map().
   */
  const safeHistory = Array.isArray(history)
    ? history
    : [];

  const chartData = safeHistory.map((weather) => {
    const timestamp =
      weather.timestamp ||
      weather.recorded_at ||
      "";

    return {
      label: timestamp
        ? new Date(timestamp).toLocaleTimeString(
            undefined,
            {
              hour: "numeric",
              minute: "2-digit",
            }
          )
        : "—",

      temperature:
        Number(weather.temperature) || 0,

      humidity:
        Number(weather.humidity) || 0,

      wind_speed:
        Number(weather.wind_speed) || 0,

      rainfall:
        Number(weather.rainfall) || 0,
    };
  });

  const latestSensitivity =
    data?.recommendations?.[0]
      ?.recommended_sensitivity ?? null;

  /*
   * Dashboard-level loading state.
   */
  if (error && !data) {
    return (
      <div className="page">
        <div className="page__header">
          <div>
            <h1>Dashboard</h1>
            <p>
              Environmental monitoring & AI
              calibration overview
            </p>
          </div>
        </div>

        <div className="panel">
          <ErrorState
            title="Unable to load dashboard"
            description={error}
            onRetry={refetch}
          />
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      {/* ================= HEADER ================= */}

      <div className="page__header">
        <div>
          <h1>Dashboard</h1>
          <p>
            Environmental monitoring & AI
            calibration overview
          </p>
        </div>
      </div>

      {/* ================= KPI SECTION ================= */}

      {loading && !data ? (
        <div className="kpi-grid">
          {Array.from({ length: 6 }).map(
            (_, index) => (
              <div
                className="panel"
                key={index}
              >
                <CardSkeleton lines={1} />
              </div>
            )
          )}
        </div>
      ) : (
        <div className="kpi-grid">
          <KpiCard
            label="Total Sensors"
            value={
              data?.total_sensors ?? "—"
            }
            icon={
              <Radio size={18} />
            }
            tone="accent"
          />

          <KpiCard
            label="Active"
            value={
              data?.active_sensors ?? "—"
            }
            icon={
              <CheckCircle2 size={18} />
            }
            tone="low"
          />

          <KpiCard
            label="Inactive"
            value={
              data?.inactive_sensors ?? "—"
            }
            icon={
              <PowerOff size={18} />
            }
            tone="neutral"
          />

          <KpiCard
            label="Active Alerts"
            value={
              data?.active_alerts ?? "—"
            }
            icon={
              <BellRing size={18} />
            }
            tone={
              data &&
              data.active_alerts > 0
                ? "high"
                : "low"
            }
          />

          <div className="panel kpi-gauge-card">
            <RiskGauge
              risk={
                data?.latest_weather
                  ?.weather_risk
              }
            />
          </div>

          <div className="panel kpi-sensitivity-card">
            <div className="kpi-sensitivity-card__label">
              Recommended Sensitivity
            </div>

            {latestSensitivity ? (
              <SensitivityBadge
                value={latestSensitivity}
              />
            ) : (
              <span className="kpi-sensitivity-card__empty">
                No recommendation yet
              </span>
            )}

            <Gauge
              size={16}
              className="kpi-sensitivity-card__icon"
            />
          </div>
        </div>
      )}

      {/* ================= WEATHER + CHARTS ================= */}

      <div className="dashboard-row dashboard-row--weather">
        <WeatherCard
          weather={data?.latest_weather}
          loading={loading}
          error={error}
          onRetry={refetch}
        />

        <div className="dashboard-charts-2col">
          <ChartCard
            title="Temperature Trend"
            data={chartData}
            dataKey="temperature"
            color="var(--accent)"
            unit="°C"
            loading={historyLoading}
            error={historyError}
            onRetry={refetchHistory}
            valueFormatter={(value) =>
              `${value.toFixed(1)}°C`
            }
          />

          <ChartCard
            title="Humidity Trend"
            data={chartData}
            dataKey="humidity"
            color="#5b9dfb"
            unit="%"
            loading={historyLoading}
            error={historyError}
            onRetry={refetchHistory}
            valueFormatter={(value) =>
              `${Math.round(value)}%`
            }
          />
        </div>
      </div>

      {/* ================= MORE CHARTS ================= */}

      <div
        className="dashboard-charts-2col"
        style={{ marginTop: 18 }}
      >
        <ChartCard
          title="Wind Speed Trend"
          data={chartData}
          dataKey="wind_speed"
          color="#c084fc"
          unit=" m/s"
          loading={historyLoading}
          error={historyError}
          onRetry={refetchHistory}
          valueFormatter={(value) =>
            `${value.toFixed(1)} m/s`
          }
        />

        <ChartCard
          title="Rainfall Trend"
          data={chartData}
          dataKey="rainfall"
          color="#38bdf8"
          unit=" mm"
          loading={historyLoading}
          error={historyError}
          onRetry={refetchHistory}
          valueFormatter={(value) =>
            `${value.toFixed(2)} mm`
          }
        />
      </div>

      {/* ================= BOTTOM SECTION ================= */}

      <div
        className="dashboard-row dashboard-row--bottom"
        style={{ marginTop: 18 }}
      >
        {/* AI RECOMMENDATIONS */}

        <div className="panel">
          <div className="panel__header">
            <h3>AI Recommendations</h3>

            <span className="panel__header-sub">
              {data?.recommendations
                ?.length ?? 0}{" "}
              active
            </span>
          </div>

          {loading && !data ? (
            <CardSkeleton lines={3} />
          ) : data &&
            data.recommendations &&
            data.recommendations.length > 0 ? (
            <div>
              {data.recommendations
                .slice(0, 5)
                .map((recommendation) => (
                  <RecommendationCard
                    key={
                      recommendation.id
                    }
                    rec={recommendation}
                  />
                ))}
            </div>
          ) : (
            <EmptyState
              title="No recommendations yet"
              description="The AI model will generate calibration recommendations once predictions run."
            />
          )}
        </div>

        {/* RECENT ALERTS */}

        <div className="panel">
          <div className="panel__header">
            <h3>Recent Alerts</h3>

            <span className="panel__header-sub">
              {data?.latest_weather
                ? `As of ${formatDateTime(
                    data.latest_weather
                      .timestamp ||
                      data.latest_weather
                        .recorded_at
                  )}`
                : ""}
            </span>
          </div>

          {loading && !data ? (
            <CardSkeleton lines={3} />
          ) : data &&
            data.recent_alerts &&
            data.recent_alerts.length > 0 ? (
            <div>
              {data.recent_alerts
                .slice(0, 5)
                .map((alert) => (
                  <AlertRow
                    key={alert.id}
                    alert={alert}
                  />
                ))}
            </div>
          ) : (
            <EmptyState
              title="No active alerts"
              description="All monitored locations are currently within acceptable environmental conditions."
            />
          )}
        </div>
      </div>
    </div>
  );
}