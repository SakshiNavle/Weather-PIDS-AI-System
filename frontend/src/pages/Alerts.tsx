import { useState } from "react";

import { useAlerts } from "../hooks/useAlerts";

import { RiskBadge } from "../components/common/RiskBadge";
import { StatusBadge } from "../components/common/StatusBadge";
import {
  EmptyState,
  ErrorState,
} from "../components/common/States";

import { AlertDetailModal } from "../components/alerts/AlertDetailModal";

import { formatRelativeTime } from "../utils/format";

import type { Alert } from "../types/alert";


export default function Alerts() {

  const {
    data,
    loading,
    error,
    refetch,
  } = useAlerts();

  const [selected, setSelected] =
    useState<Alert | null>(null);


  // ============================================================
  // LOADING
  // ============================================================

  if (loading && !data) {

    return (
      <div className="page">

        <div className="page-header">

          <div>

            <h1>Alerts</h1>

            <p>
              Weather-risk alerts raised
              for monitored sites
            </p>

          </div>

        </div>

        <div className="panel">

          <div
            style={{
              padding: 18,
              color: "var(--text-tertiary)",
              fontSize: 13,
            }}
          >
            Loading alerts...
          </div>

        </div>

      </div>
    );
  }


  // ============================================================
  // ERROR
  // ============================================================

  if (error && !data) {

    return (
      <div className="page">

        <div className="page-header">

          <div>

            <h1>Alerts</h1>

            <p>
              Weather-risk alerts raised
              for monitored sites
            </p>

          </div>

        </div>

        <ErrorState
          title="Unable to load alerts."
          description={error}
          onRetry={refetch}
        />

      </div>
    );
  }


  // ============================================================
  // MAIN
  // ============================================================

  return (

    <div className="page">

      {/* ======================================================
          HEADER
      ====================================================== */}

      <div className="page-header">

        <div>

          <h1>Alerts</h1>

          <p>
            Weather-risk alerts raised
            for monitored sites
          </p>

        </div>

      </div>


      {/* ======================================================
          ALERT TABLE
      ====================================================== */}

      <div className="panel">

        {data && data.length > 0 ? (

          <div className="data-table-wrap">

            <table className="data-table">

              <thead>

                <tr>

                  <th>Risk</th>

                  <th>Site</th>

                  <th>Message</th>

                  <th>Status</th>

                  <th>Created</th>

                  <th></th>

                </tr>

              </thead>


              <tbody>

                {data.map((alert) => (

                  <tr key={alert.id}>

                    {/* RISK */}

                    <td>

                      <RiskBadge
                        risk={alert.risk_level}
                        size="sm"
                      />

                    </td>


                    {/* SITE */}

                    <td className="cell-secondary">

                      {alert.site_name || "—"}

                    </td>


                    {/* MESSAGE */}

                    <td
                      style={{
                        maxWidth: 340,
                      }}
                    >

                      {alert.message}

                    </td>


                    {/* STATUS */}

                    <td>

                      <StatusBadge
                        status={
                          alert.is_active
                            ? "ACTIVE"
                            : "INACTIVE"
                        }
                      />

                    </td>


                    {/* CREATED */}

                    <td className="cell-mono">

                      {alert.created_at
                        ? formatRelativeTime(
                            alert.created_at
                          )
                        : "—"}

                    </td>


                    {/* VIEW */}

                    <td>

                      <button
                        className="link-btn"
                        onClick={() =>
                          setSelected(alert)
                        }
                      >
                        View
                      </button>

                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        ) : (

          <EmptyState

            title="No active alerts"

            description={
              "All monitored locations are currently " +
              "within acceptable environmental conditions."
            }

          />

        )}

      </div>


      {/* ======================================================
          DETAIL MODAL
      ====================================================== */}

      {selected && (

        <AlertDetailModal
          alert={selected}
          onClose={() =>
            setSelected(null)
          }
        />

      )}

    </div>
  );
}