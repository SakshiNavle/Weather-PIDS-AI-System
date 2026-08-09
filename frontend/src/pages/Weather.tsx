import { useWeatherHistory } from "../hooks/useWeather";
import { WeatherCard } from "../components/weather/WeatherCard";
import { ChartCard } from "../components/weather/ChartCard";
import { EmptyState, ErrorState } from "../components/common/States";
import { formatDateTime } from "../utils/format";
import { RiskBadge } from "../components/common/RiskBadge";

export default function Weather() {
  const {
    data: history,
    loading,
    error,
    refetch,
  } = useWeatherHistory(72);

  const weatherHistory = Array.isArray(history) ? history : [];

  const chartData = weatherHistory
    .slice()
    .reverse()
    .map((w) => {
      const timestamp =
        w.timestamp || new Date().toISOString();

      return {
        label: new Date(timestamp).toLocaleTimeString(undefined, {
          hour: "numeric",
          minute: "2-digit",
        }),
        temperature: Number(w.temperature) || 0,
        humidity: Number(w.humidity) || 0,
        wind_speed: Number(w.wind_speed) || 0,
        rainfall: Number(w.rainfall) || 0,
      };
    })
    .reverse();

  const latest =
    weatherHistory.length > 0
      ? weatherHistory[0]
      : null;

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Weather</h1>
          <p>
            Live environmental readings feeding the calibration model
          </p>
        </div>
      </div>

      <div className="dashboard-row dashboard-row--weather">
        <WeatherCard
          weather={latest}
          loading={loading}
          error={error}
          onRetry={refetch}
        />

        <div className="panel">
          <div className="panel__header">
            <h3>Weather History</h3>

            <span className="panel__header-sub">
              {loading
                ? "Loading..."
                : `${weatherHistory.length} readings`}
            </span>
          </div>

          {loading && weatherHistory.length === 0 ? (
            <div
              style={{
                padding: 18,
                color: "var(--text-tertiary)",
                fontSize: 13,
              }}
            >
              Loading weather history...
            </div>
          ) : error && weatherHistory.length === 0 ? (
            <ErrorState
              title="Unable to load weather history."
              description={error}
              onRetry={refetch}
            />
          ) : weatherHistory.length > 0 ? (
            <div
              className="data-table-wrap"
              style={{
                maxHeight: 320,
                overflowY: "auto",
              }}
            >
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Site</th>
                    <th>Condition</th>
                    <th>Temp</th>
                    <th>Humidity</th>
                    <th>Wind</th>
                    <th>Risk</th>
                    <th>Time</th>
                  </tr>
                </thead>

                <tbody>
                  {weatherHistory
                    .slice(0, 20)
                    .map((w) => (
                      <tr key={w.id}>
                        <td>{w.site_name}</td>

                        <td className="cell-secondary">
                          {w.weather_condition}
                        </td>

                        <td className="cell-mono">
                          {Number(w.temperature).toFixed(1)}°C
                        </td>

                        <td className="cell-mono">
                          {Number(w.humidity).toFixed(0)}%
                        </td>

                        <td className="cell-mono">
                          {Number(w.wind_speed).toFixed(1)} m/s
                        </td>

                        <td>
                          <RiskBadge
                            risk={w.weather_risk}
                            size="sm"
                          />
                        </td>

                        <td className="cell-mono">
                          {formatDateTime(w.timestamp)}
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          ) : (
            <EmptyState
              title="No weather history yet"
              description="Readings will appear here as the scheduler collects data."
            />
          )}
        </div>
      </div>

      <div
        className="dashboard-charts-2col"
        style={{ marginTop: 18 }}
      >
        <ChartCard
          title="Temperature vs Time"
          data={chartData}
          dataKey="temperature"
          color="var(--accent)"
          unit="°C"
          loading={loading}
          error={error}
          onRetry={refetch}
          valueFormatter={(v) => `${v.toFixed(1)}°C`}
        />

        <ChartCard
          title="Humidity vs Time"
          data={chartData}
          dataKey="humidity"
          color="#5b9dfb"
          unit="%"
          loading={loading}
          error={error}
          onRetry={refetch}
          valueFormatter={(v) => `${Math.round(v)}%`}
        />
      </div>

      <div
        className="dashboard-charts-2col"
        style={{ marginTop: 18 }}
      >
        <ChartCard
          title="Wind Speed vs Time"
          data={chartData}
          dataKey="wind_speed"
          color="#c084fc"
          unit=" m/s"
          loading={loading}
          error={error}
          onRetry={refetch}
          valueFormatter={(v) => `${v.toFixed(1)} m/s`}
        />

        <ChartCard
          title="Rainfall vs Time"
          data={chartData}
          dataKey="rainfall"
          color="#38bdf8"
          unit=" mm"
          loading={loading}
          error={error}
          onRetry={refetch}
          valueFormatter={(v) => `${v.toFixed(2)} mm`}
        />
      </div>
    </div>
  );
}