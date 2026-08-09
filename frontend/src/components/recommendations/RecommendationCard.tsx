import { Sparkles } from "lucide-react";

import type { Recommendation } from "../../types/recommendation";

import { RiskBadge } from "../common/RiskBadge";
import { SensitivityBadge } from "../common/SensitivityBadge";
import { formatRelativeTime } from "../../utils/format";

import "./recommendation-card.css";

export function RecommendationCard({
  rec,
}: {
  rec: Recommendation;
}) {
  return (
    <div className="recommendation-card">

      <div className="recommendation-card__header">

        <div className="recommendation-card__title">
          <Sparkles size={18} />

          <div>
            <h3>
              {rec.title}
            </h3>

            <span>
              Sensor #{rec.sensor_id}
            </span>
          </div>
        </div>

        <RiskBadge
          risk={rec.risk_level}
          size="sm"
        />

      </div>

      <div className="recommendation-card__body">

        <p>
          {rec.description}
        </p>

        {rec.action && (
          <div className="recommendation-card__action">
            <strong>Recommended Action:</strong>

            <span>
              {rec.action}
            </span>
          </div>
        )}

        {rec.recommended_sensitivity && (
          <div className="recommendation-card__sensitivity">

            <span>
              Recommended Sensitivity:
            </span>

            <SensitivityBadge
              value={
                rec.recommended_sensitivity
              }
            />

          </div>
        )}

      </div>

      <div className="recommendation-card__footer">

        <span>
          Created{" "}
          {formatRelativeTime(rec.created_at)}
        </span>

      </div>

    </div>
  );
}