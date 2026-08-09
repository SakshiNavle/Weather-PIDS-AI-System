import { useMemo, useState } from "react";
import {
  Activity,
  AlertTriangle,
  CheckCircle2,
  Gauge,
  Sparkles,
} from "lucide-react";

import { useRecommendations } from "../hooks/useRecommendations";
import { recommendationApi } from "../api/recommendationApi";
import { RecommendationCard } from "../components/recommendations/RecommendationCard";
import {
  EmptyState,
  ErrorState,
  CardSkeleton,
} from "../components/common/States";

import type { Recommendation } from "../types/recommendation";
import type { RiskLevel } from "../types/weather";

import "../styles/recommendations.css";

type Filter = "ALL" | RiskLevel;

const FILTERS: Filter[] = [
  "ALL",
  "LOW",
  "MEDIUM",
  "HIGH",
  "SEVERE",
];

export default function Recommendations() {
  const {
    data,
    loading,
    error,
    refetch,
  } = useRecommendations();

  const [filter, setFilter] = useState<Filter>("ALL");
  const [filtered, setFiltered] = useState<Recommendation[] | null>(
    null
  );

  const [filterLoading, setFilterLoading] = useState(false);
  const [filterError, setFilterError] = useState<string | null>(
    null
  );

  const recommendations = Array.isArray(data) ? data : [];

  /*
   * ---------------------------------------------------------
   * FILTER
   * ---------------------------------------------------------
   */

  const applyFilter = async (next: Filter) => {
    setFilter(next);

    if (next === "ALL") {
      setFiltered(null);
      setFilterError(null);
      return;
    }

    setFilterLoading(true);
    setFilterError(null);

    try {
      const result = await recommendationApi.byRisk(next);

      setFiltered(
        Array.isArray(result) ? result : []
      );
    } catch (err) {
      setFilterError(
        err instanceof Error
          ? err.message
          : "Unable to filter recommendations."
      );

      setFiltered([]);
    } finally {
      setFilterLoading(false);
    }
  };

  const list =
    filter === "ALL"
      ? recommendations
      : filtered ?? [];

  const isLoading =
    filter === "ALL"
      ? loading
      : filterLoading;

  const isError =
    filter === "ALL"
      ? error
      : filterError;

  /*
   * ---------------------------------------------------------
   * SUMMARY
   * ---------------------------------------------------------
   */

  const stats = useMemo(() => {
    return {
      total: recommendations.length,

      low: recommendations.filter(
        (r) =>
          r.risk_level?.toUpperCase() === "LOW"
      ).length,

      medium: recommendations.filter(
        (r) =>
          r.risk_level?.toUpperCase() === "MEDIUM"
      ).length,

      high: recommendations.filter(
        (r) =>
          r.risk_level?.toUpperCase() === "HIGH"
      ).length,

      severe: recommendations.filter(
        (r) =>
          r.risk_level?.toUpperCase() === "SEVERE"
      ).length,
    };
  }, [recommendations]);

  /*
   * ---------------------------------------------------------
   * CURRENT STATUS
   * ---------------------------------------------------------
   */

  const dominantRisk =
    stats.severe > 0
      ? "SEVERE"
      : stats.high > 0
      ? "HIGH"
      : stats.medium > 0
      ? "MEDIUM"
      : "LOW";

  return (
    <div className="recommendations-page">

      {/* =====================================================
          HEADER
      ===================================================== */}

      <div className="recommendations-header">

        <div>
          <div className="page-eyebrow">
            <Sparkles size={14} />
            AI CALIBRATION ENGINE
          </div>

          <h1>
            Recommendations
          </h1>

          <p>
            AI-generated sensor calibration guidance
            based on current environmental conditions.
          </p>
        </div>

        <div className="recommendation-status">

          <div className="recommendation-status__icon">
            <Activity size={20} />
          </div>

          <div>
            <span>Current risk profile</span>

            <strong
              className={`risk-text risk-text--${dominantRisk.toLowerCase()}`}
            >
              {dominantRisk}
            </strong>
          </div>

        </div>

      </div>


      {/* =====================================================
          SUMMARY CARDS
      ===================================================== */}

      <div className="recommendation-summary">

        <div className="summary-card">

          <div className="summary-card__icon">
            <Gauge size={19} />
          </div>

          <div>
            <span>Total Recommendations</span>
            <strong>{stats.total}</strong>
          </div>

        </div>


        <div className="summary-card summary-card--low">

          <div className="summary-card__icon">
            <CheckCircle2 size={19} />
          </div>

          <div>
            <span>Low Risk</span>
            <strong>{stats.low}</strong>
          </div>

        </div>


        <div className="summary-card summary-card--medium">

          <div className="summary-card__icon">
            <Activity size={19} />
          </div>

          <div>
            <span>Medium Risk</span>
            <strong>{stats.medium}</strong>
          </div>

        </div>


        <div className="summary-card summary-card--high">

          <div className="summary-card__icon">
            <AlertTriangle size={19} />
          </div>

          <div>
            <span>High / Severe</span>

            <strong>
              {stats.high + stats.severe}
            </strong>
          </div>

        </div>

      </div>


      {/* =====================================================
          FILTER BAR
      ===================================================== */}

      <div className="recommendation-toolbar">

        <div>
          <span className="toolbar-label">
            Filter by risk
          </span>

          <div className="filter-chips">

            {FILTERS.map((f) => {

              const count =
                f === "ALL"
                  ? stats.total
                  : f === "LOW"
                  ? stats.low
                  : f === "MEDIUM"
                  ? stats.medium
                  : f === "HIGH"
                  ? stats.high
                  : stats.severe;

              return (
                <button
                  key={f}
                  className={`filter-chip ${
                    filter === f
                      ? "filter-chip--active"
                      : ""
                  }`}
                  onClick={() => applyFilter(f)}
                >

                  <span>
                    {f}
                  </span>

                  <small>
                    {count}
                  </small>

                </button>
              );
            })}

          </div>
        </div>

        <div className="recommendation-count">
          Showing{" "}
          <strong>{list.length}</strong>{" "}
          recommendation
          {list.length !== 1 ? "s" : ""}
        </div>

      </div>


      {/* =====================================================
          CONTENT
      ===================================================== */}

      <div className="recommendations-content">

        {isLoading && !list.length ? (

          <div className="recommendation-loading">
            <CardSkeleton lines={4} />
            <CardSkeleton lines={4} />
          </div>

        ) : isError && !list.length ? (

          <ErrorState
            title="Unable to load recommendations."
            description={isError}
            onRetry={
              filter === "ALL"
                ? refetch
                : () => applyFilter(filter)
            }
          />

        ) : list.length > 0 ? (

          <div className="recommendation-list">

            {list.map((rec) => (
              <RecommendationCard
                key={rec.id}
                rec={rec}
              />
            ))}

          </div>

        ) : (

          <div className="recommendation-empty">

            <EmptyState
              title={
                filter === "ALL"
                  ? "No recommendations yet"
                  : `No ${filter.toLowerCase()}-risk recommendations`
              }
              description={
                filter === "ALL"
                  ? "Recommendations will appear when the calibration engine evaluates sensor and weather conditions."
                  : `There are currently no ${filter.toLowerCase()}-risk calibration recommendations.`
              }
            />

          </div>

        )}

      </div>

    </div>
  );
}