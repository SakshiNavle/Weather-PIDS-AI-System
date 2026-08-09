import { Sparkles } from "lucide-react";
import type { Recommendation } from "../../types/recommendation";
import { RiskBadge } from "../common/RiskBadge";
import { SensitivityBadge } from "../common/SensitivityBadge";
import { formatRelativeTime } from "../../utils/format";
import "./recommendation-card.css";

export function RecommendationCard({ rec }: { rec: Recommendation }) {
  return (
    <div className="rec-card">
      <div className="rec-card__icon">
        <Sparkles size={15} />
      </div>
      <div className="rec-card__body">
        <div className="rec-card__top">
          <span className="rec-card__title">
            {rec.sensor_name ? `${rec.sensor_name} Calibration` : `Sensor #${rec.sensor_id} Calibration`}
          </span>
          <RiskBadge risk={rec.risk} size="sm" />
        </div>
        <p className="rec-card__message">{rec.message}</p>
        <div className="rec-card__footer">
          <span className="rec-card__action">
            Recommended: <SensitivityBadge value={rec.recommended_sensitivity} />
          </span>
          <span className="rec-card__time">{formatRelativeTime(rec.created_at)}</span>
        </div>
      </div>
    </div>
  );
}
