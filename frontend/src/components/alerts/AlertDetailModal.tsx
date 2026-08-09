import { Modal } from "../common/Modal";
import { RiskBadge } from "../common/RiskBadge";
import { StatusBadge } from "../common/StatusBadge";
import { formatDateTime } from "../../utils/format";
import type { Alert } from "../../types/alert";

interface AlertDetailModalProps {
  alert: Alert;
  onClose: () => void;
}

export function AlertDetailModal({ alert, onClose }: AlertDetailModalProps) {
  return (
    <Modal title="Alert Details" onClose={onClose} footer={<button className="btn btn--ghost" onClick={onClose}>Close</button>}>
      <dl className="kv-list" style={{ padding: 0 }}>
        {alert.site_name && (
          <div>
            <dt>Location</dt>
            <dd>{alert.site_name}</dd>
          </div>
        )}
        <div>
          <dt>Risk Level</dt>
          <dd><RiskBadge risk={alert.risk} size="sm" /></dd>
        </div>
        <div>
          <dt>Current Status</dt>
          <dd><StatusBadge status={alert.status} /></dd>
        </div>
        <div>
          <dt>Created At</dt>
          <dd>{formatDateTime(alert.created_at)}</dd>
        </div>
      </dl>
      <p style={{ fontSize: 13, color: "var(--text-secondary)", lineHeight: 1.6, marginTop: 12 }}>
        {alert.message}
      </p>
    </Modal>
  );
}
