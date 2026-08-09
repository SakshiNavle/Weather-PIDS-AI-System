import { useBackendStatus } from "../hooks/useBackendStatus";

export default function Settings() {
  const status = useBackendStatus();
  const baseUrl = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1";

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Settings</h1>
          <p>Backend connection and system information</p>
        </div>
      </div>

      <div className="panel" style={{ maxWidth: 560 }}>
        <div className="panel__header">
          <h3>Backend Connection</h3>
        </div>
        <dl className="kv-list">
          <div>
            <dt>API Base URL</dt>
            <dd className="mono">{baseUrl}</dd>
          </div>
          <div>
            <dt>Status</dt>
            <dd style={{ textTransform: "capitalize" }}>{status}</dd>
          </div>
          <div>
            <dt>Auto Refresh</dt>
            <dd>Dashboard 30s · Weather 60s · Alerts 30s · Sensors 60s</dd>
          </div>
        </dl>
      </div>

      <div className="panel" style={{ maxWidth: 560, marginTop: 18 }}>
        <div className="panel__header">
          <h3>About</h3>
        </div>
        <p style={{ padding: "0 18px 18px", fontSize: 13, color: "var(--text-secondary)", lineHeight: 1.6, margin: 0 }}>
          PIDS Calibration AI monitors environmental conditions and recommends sensor
          sensitivity to reduce false intrusion alarms caused by weather. All data
          shown throughout this dashboard is read live from the FastAPI backend —
          nothing here is hardcoded.
        </p>
      </div>
    </div>
  );
}
