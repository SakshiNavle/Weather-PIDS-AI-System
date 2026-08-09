import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { ArrowLeft, Zap } from "lucide-react";
import { sensorApi } from "../api/sensorApi";
import { predictionApi } from "../api/predictionApi";
import type { Sensor } from "../types/sensor";
import type { Prediction } from "../types/prediction";
import { StatusBadge } from "../components/common/StatusBadge";
import { SensitivityBadge } from "../components/common/SensitivityBadge";
import { EmptyState, ErrorState, CardSkeleton } from "../components/common/States";
import { useToast } from "../components/common/ToastContext";
import { formatConfidence, formatDateTime, formatRelativeTime, confidenceToPercent } from "../utils/format";

export default function SensorDetails() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { showToast } = useToast();

  const [sensor, setSensor] = useState<Sensor | null>(null);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [running, setRunning] = useState(false);

  const load = async () => {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      const [sensorRes, predRes] = await Promise.all([
        sensorApi.get(Number(id)),
        predictionApi.bySensor(id).catch(() => []),
      ]);
      setSensor(sensorRes);
      setPredictions(predRes);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load sensor.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const runPrediction = async () => {
    if (!id) return;
    setRunning(true);
    try {
      await predictionApi.run(id);
      showToast("Prediction completed successfully", "success");
      await load();
    } catch (err) {
      const message = err instanceof Error ? err.message : "Prediction failed.";
      showToast(message, "error");
    } finally {
      setRunning(false);
    }
  };

  const latest = predictions[0];

  return (
    <div>
      <button className="link-btn" style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 14 }} onClick={() => navigate("/sensors")}>
        <ArrowLeft size={14} />
        Back to Sensors
      </button>

      {loading && !sensor ? (
        <div className="panel">
          <CardSkeleton lines={5} />
        </div>
      ) : error && !sensor ? (
        <div className="panel">
          <ErrorState title="Unable to load sensor." description={error} onRetry={load} />
        </div>
      ) : sensor ? (
        <>
          <div className="page-header">
            <div>
              <h1>{sensor.name}</h1>
              <p>
                {sensor.sensor_type} · {sensor.location}
              </p>
            </div>
            <div className="page-header__actions">
              <button className="btn btn--primary" onClick={runPrediction} disabled={running}>
                <Zap size={14} />
                {running ? "Running AI prediction..." : "Run Prediction"}
              </button>
            </div>
          </div>

          <div className="sensor-detail-grid">
            <div className="panel">
              <div className="panel__header">
                <h3>Sensor Information</h3>
              </div>
              <dl className="kv-list">
                <div><dt>Sensor ID</dt><dd className="mono">{sensor.id}</dd></div>
                <div><dt>Sensor Name</dt><dd>{sensor.name}</dd></div>
                <div><dt>Sensor Type</dt><dd>{sensor.sensor_type}</dd></div>
                <div><dt>Location</dt><dd>{sensor.location}</dd></div>
                <div><dt>Status</dt><dd><StatusBadge status={sensor.status} /></dd></div>
                <div><dt>Current Sensitivity</dt><dd><SensitivityBadge value={sensor.sensitivity} /></dd></div>
              </dl>
            </div>

            <div className="panel">
              <div className="panel__header">
                <h3>Latest AI Prediction</h3>
              </div>
              {latest ? (
                <div className="latest-prediction">
                  <div className="latest-prediction__row">
                    <span>Recommended Sensitivity</span>
                    <SensitivityBadge value={latest.recommended_sensitivity} />
                  </div>
                  <div className="latest-prediction__row">
                    <span>Confidence Score</span>
                    <span className="mono">{formatConfidence(latest.confidence)}</span>
                  </div>
                  <div className="confidence-bar">
                    <div
                      className="confidence-bar__fill"
                      style={{ width: `${confidenceToPercent(latest.confidence)}%` }}
                    />
                  </div>
                  {latest.explanation && <p className="latest-prediction__explanation">{latest.explanation}</p>}
                  <div className="latest-prediction__row latest-prediction__row--muted">
                    <span>Created At</span>
                    <span>{formatDateTime(latest.created_at)}</span>
                  </div>
                </div>
              ) : (
                <EmptyState title="No predictions yet" description="Run a prediction to get an AI calibration recommendation." />
              )}
            </div>
          </div>

          <div className="panel" style={{ marginTop: 18 }}>
            <div className="panel__header">
              <h3>Prediction History</h3>
              <span className="panel__header-sub">{predictions.length} records</span>
            </div>
            {predictions.length > 0 ? (
              <div className="data-table-wrap">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Recommended</th>
                      <th>Confidence</th>
                      <th>Explanation</th>
                      <th>Created</th>
                    </tr>
                  </thead>
                  <tbody>
                    {predictions.map((p) => (
                      <tr key={p.id}>
                        <td><SensitivityBadge value={p.recommended_sensitivity} /></td>
                        <td className="cell-mono">{formatConfidence(p.confidence)}</td>
                        <td className="cell-secondary" style={{ maxWidth: 320 }}>{p.explanation || "—"}</td>
                        <td className="cell-mono">{formatRelativeTime(p.created_at)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <EmptyState title="No prediction history" description="This sensor hasn't had any AI predictions run yet." />
            )}
          </div>
        </>
      ) : (
        <div className="panel">
          <EmptyState title="Sensor not found" description="It may have been removed." />
          <div style={{ textAlign: "center", paddingBottom: 18 }}>
            <Link to="/sensors" className="link-btn">Return to sensors list</Link>
          </div>
        </div>
      )}
    </div>
  );
}
