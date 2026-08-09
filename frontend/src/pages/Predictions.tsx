import { useState } from "react";
import { Zap, PlayCircle } from "lucide-react";
import { usePredictions } from "../hooks/usePredictions";
import { useSensors } from "../hooks/useSensors";
import { predictionApi } from "../api/predictionApi";
import { SensitivityBadge } from "../components/common/SensitivityBadge";
import { EmptyState, ErrorState } from "../components/common/States";
import { useToast } from "../components/common/ToastContext";
import { formatConfidence, formatRelativeTime, confidenceToPercent } from "../utils/format";
import type { RunAllResult } from "../types/prediction";

export default function Predictions() {
  const { data: predictions, loading, error, refetch } = usePredictions();
  const { data: sensors, refetch: refetchSensors } = useSensors();
  const { showToast } = useToast();
  const [runningAll, setRunningAll] = useState(false);
  const [runningSensor, setRunningSensor] = useState<number | null>(null);
  const [lastRunAll, setLastRunAll] = useState<RunAllResult | null>(null);

  const sensorName = (sensorId: number) =>
    sensors?.find((s) => s.id === sensorId)?.name ?? `Sensor #${sensorId}`;

  const runOne = async (sensorId: number) => {
    setRunningSensor(sensorId);
    try {
      await predictionApi.run(sensorId);
      showToast("Prediction completed successfully", "success");
      await refetch();
      await refetchSensors();
    } catch (err) {
      showToast(err instanceof Error ? err.message : "Prediction failed.", "error");
    } finally {
      setRunningSensor(null);
    }
  };

  const runAll = async () => {
    setRunningAll(true);
    setLastRunAll(null);
    try {
      const result = await predictionApi.runAll();
      setLastRunAll(result);
      showToast(`${result.processed} sensors processed`, "success");
      await refetch();
      await refetchSensors();
    } catch (err) {
      showToast(err instanceof Error ? err.message : "Run all predictions failed.", "error");
    } finally {
      setRunningAll(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>AI Calibration Predictions</h1>
          <p>Model-recommended sensitivity for each registered sensor</p>
        </div>
        <div className="page-header__actions">
          <button className="btn btn--ghost" onClick={runAll} disabled={runningAll}>
            <PlayCircle size={15} />
            {runningAll ? "Processing sensors..." : "Run All Predictions"}
          </button>
        </div>
      </div>

      {lastRunAll && (
        <div className="panel" style={{ padding: "12px 16px", marginBottom: 16, fontSize: 13 }}>
          <strong>{lastRunAll.processed} sensors processed</strong>
          <span style={{ color: "var(--text-tertiary)" }}>
            {" "}
            · {lastRunAll.successful} successful · {lastRunAll.failed} failed
          </span>
          {lastRunAll.failed_sensors && lastRunAll.failed_sensors.length > 0 && (
            <ul style={{ margin: "8px 0 0", paddingLeft: 18, color: "var(--risk-high)", fontSize: 12.5 }}>
              {lastRunAll.failed_sensors.map((f) => (
                <li key={f.sensor_id}>
                  {f.sensor_name ?? `Sensor #${f.sensor_id}`}
                  {f.reason ? ` — ${f.reason}` : ""}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      <div className="panel">
        {loading && !predictions ? (
          <div style={{ padding: 18, color: "var(--text-tertiary)", fontSize: 13 }}>Loading predictions...</div>
        ) : error && !predictions ? (
          <ErrorState title="Unable to load predictions." description={error} onRetry={refetch} />
        ) : predictions && predictions.length > 0 ? (
          <div className="data-table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Sensor</th>
                  <th>Recommended Sensitivity</th>
                  <th style={{ minWidth: 140 }}>Confidence</th>
                  <th>Explanation</th>
                  <th>Created</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {predictions.map((p) => (
                  <tr key={p.id}>
                    <td style={{ fontWeight: 600 }}>{p.sensor_name ?? sensorName(p.sensor_id)}</td>
                    <td><SensitivityBadge value={p.recommended_sensitivity} /></td>
                    <td>
                      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                        <div className="confidence-bar" style={{ flex: 1, margin: 0 }}>
                          <div
                            className="confidence-bar__fill"
                            style={{ width: `${confidenceToPercent(p.confidence)}%` }}
                          />
                        </div>
                        <span className="cell-mono">{formatConfidence(p.confidence)}</span>
                      </div>
                    </td>
                    <td className="cell-secondary" style={{ maxWidth: 260 }}>{p.explanation || "—"}</td>
                    <td className="cell-mono">{formatRelativeTime(p.created_at)}</td>
                    <td>
                      <button
                        className="icon-btn"
                        aria-label="Re-run prediction"
                        onClick={() => runOne(p.sensor_id)}
                        disabled={runningSensor === p.sensor_id}
                      >
                        <Zap size={14} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <EmptyState
            title="No predictions yet"
            description="Run predictions for your sensors to see AI calibration recommendations here."
          />
        )}
      </div>
    </div>
  );
}
