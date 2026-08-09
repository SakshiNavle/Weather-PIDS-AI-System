import { useState } from "react";
import { useRecommendations } from "../hooks/useRecommendations";
import { recommendationApi } from "../api/recommendationApi";
import { RecommendationCard } from "../components/recommendations/RecommendationCard";
import { EmptyState, ErrorState, CardSkeleton } from "../components/common/States";
import type { Recommendation } from "../types/recommendation";
import type { RiskLevel } from "../types/weather";

const FILTERS: Array<"ALL" | RiskLevel> = ["ALL", "LOW", "MEDIUM", "HIGH", "SEVERE"];

export default function Recommendations() {
  const { data, loading, error } = useRecommendations();
  const [filter, setFilter] = useState<"ALL" | RiskLevel>("ALL");
  const [filtered, setFiltered] = useState<Recommendation[] | null>(null);
  const [filterLoading, setFilterLoading] = useState(false);
  const [filterError, setFilterError] = useState<string | null>(null);

  const applyFilter = async (next: "ALL" | RiskLevel) => {
    setFilter(next);
    if (next === "ALL") {
      setFiltered(null);
      return;
    }
    setFilterLoading(true);
    setFilterError(null);
    try {
      const result = await recommendationApi.byRisk(next);
      setFiltered(result);
    } catch (err) {
      setFilterError(err instanceof Error ? err.message : "Unable to filter recommendations.");
      setFiltered(null);
    } finally {
      setFilterLoading(false);
    }
  };

  const list = filter === "ALL" ? data : filtered;
  const isLoading = filter === "ALL" ? loading : filterLoading;
  const isError = filter === "ALL" ? error : filterError;

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Recommendations</h1>
          <p>AI-generated calibration guidance by risk level</p>
        </div>
      </div>

      <div className="filter-chips">
        {FILTERS.map((f) => (
          <button
            key={f}
            className={`filter-chip ${filter === f ? "filter-chip--active" : ""}`}
            onClick={() => applyFilter(f)}
          >
            {f}
          </button>
        ))}
      </div>

      <div className="panel">
        {isLoading && !list ? (
          <CardSkeleton lines={3} />
        ) : isError && !list ? (
          <ErrorState title="Unable to load recommendations." description={isError} onRetry={() => applyFilter(filter)} />
        ) : list && list.length > 0 ? (
          <div>
            {list.map((rec) => (
              <RecommendationCard key={rec.id} rec={rec} />
            ))}
          </div>
        ) : (
          <EmptyState
            title="No recommendations"
            description={
              filter === "ALL"
                ? "The AI model hasn't generated any recommendations yet."
                : `No ${filter.toLowerCase()}-risk recommendations right now.`
            }
          />
        )}
      </div>
    </div>
  );
}
