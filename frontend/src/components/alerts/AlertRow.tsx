import { AlertOctagon } from "lucide-react";
import type { Alert } from "../../types/alert";
import { RiskBadge } from "../common/RiskBadge";
import { formatRelativeTime } from "../../utils/format";
import "./alert-row.css";

export function AlertRow({ alert, onClick }: { alert: Alert; onClick?: () => void }) {
  return (
    <button className="alert-row" onClick={onClick} disabled={!onClick}>
      <div className="alert-row__icon">
        <AlertOctagon size={15} />
      </div>
      <div className="alert-row__body">
        <div className="alert-row__top">
          <RiskBadge risk={alert.risk} size="sm" />
          {alert.site_name && <span className="alert-row__site">{alert.site_name}</span>}
        </div>
        <p className="alert-row__message">{alert.message}</p>
      </div>
      <span className="alert-row__time">{formatRelativeTime(alert.created_at)}</span>
    </button>
  );
}
