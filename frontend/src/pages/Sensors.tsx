import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Plus, Trash2 } from "lucide-react";

import { useSensors } from "../hooks/useSensors";
import { StatusBadge } from "../components/common/StatusBadge";
import { SensitivityBadge } from "../components/common/SensitivityBadge";
import {
  EmptyState,
  ErrorState,
} from "../components/common/States";
import { AddSensorModal } from "../components/sensors/AddSensorModal";
import { ConfirmDialog } from "../components/common/ConfirmDialog";
import { useToast } from "../components/common/ToastContext";

import { sensorApi } from "../api/sensorApi";

import type { Sensor } from "../types/sensor";


export default function Sensors() {

  const {
    data,
    loading,
    error,
    refetch,
  } = useSensors();

  const [showAdd, setShowAdd] = useState(false);

  const [pendingDelete, setPendingDelete] =
    useState<Sensor | null>(null);

  const navigate = useNavigate();

  const { showToast } = useToast();


  // ============================================================
  // DELETE SENSOR
  // ============================================================

  const handleDelete = async () => {

    if (!pendingDelete) {
      return;
    }

    try {

      await sensorApi.remove(
        pendingDelete.id
      );

      showToast(
        "Sensor deleted successfully.",
        "success"
      );

      await refetch();

    } catch (err) {

      const message =
        err instanceof Error
          ? err.message
          : "Could not delete sensor.";

      showToast(
        message,
        "error"
      );

    } finally {

      setPendingDelete(null);
    }
  };


  // ============================================================
  // LOADING
  // ============================================================

  if (loading && !data) {

    return (
      <div className="page">

        <div className="page-header">

          <div>

            <h1>Sensors</h1>

            <p>
              Registered PIDS sensor units and
              their calibration state
            </p>

          </div>

        </div>


        <div className="panel">

          <div style={{ padding: 18 }}>

            {Array.from({ length: 4 }).map(
              (_, index) => (

                <div
                  key={index}
                  style={{
                    height: 44,
                    background:
                      "var(--surface-2)",
                    borderRadius: 6,
                    marginBottom: 8,
                  }}
                />

              )
            )}

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

            <h1>Sensors</h1>

            <p>
              Registered PIDS sensor units and
              their calibration state
            </p>

          </div>

        </div>

        <ErrorState
          title="Unable to load sensors."
          description={error}
          onRetry={refetch}
        />

      </div>
    );
  }


  // ============================================================
  // MAIN UI
  // ============================================================

  return (

    <div className="page">

      {/* ======================================================
          HEADER
      ====================================================== */}

      <div
        className="page-header"
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          gap: 16,
        }}
      >

        <div>

          <h1>Sensors</h1>

          <p>
            Registered PIDS sensor units and
            their calibration state
          </p>

        </div>


        <button
          className="btn btn--primary"
          onClick={() => setShowAdd(true)}
        >

          <Plus size={16} />

          Add Sensor

        </button>

      </div>


      {/* ======================================================
          SENSOR TABLE
      ====================================================== */}

      <div className="panel">

        {data && data.length > 0 ? (

          <div className="data-table-wrap">

            <table className="data-table">

              <thead>

                <tr>

                  <th>Sensor</th>

                  <th>Type</th>

                  <th>Location</th>

                  <th>Status</th>

                  <th>Sensitivity</th>

                  <th>Actions</th>

                </tr>

              </thead>


              <tbody>

                {data.map((sensor) => (

                  <tr key={sensor.id}>

                    {/* SENSOR */}

                    <td>

                      <div
                        style={{
                          fontWeight: 600,
                        }}
                      >
                        {sensor.sensor_name}
                      </div>

                      <div
                        className="cell-secondary"
                        style={{
                          fontSize: 12,
                        }}
                      >
                        ID: #{sensor.id}
                      </div>

                    </td>


                    {/* TYPE */}

                    <td className="cell-secondary">

                      {sensor.sensor_type}

                    </td>


                    {/* LOCATION */}

                    <td className="cell-secondary">

                      {sensor.location}

                    </td>


                    {/* STATUS */}

                    <td>

                      <StatusBadge
                        status={sensor.status}
                      />

                    </td>


                    {/* SENSITIVITY */}

                    <td>

                      <SensitivityBadge
                        value={
                          sensor.current_sensitivity ??
                          "MEDIUM"
                        }
                      />

                    </td>


                    {/* ACTIONS */}

                    <td>

                      <div
                        style={{
                          display: "flex",
                          gap: 8,
                          justifyContent:
                            "flex-end",
                        }}
                      >

                        <button
                          className="link-btn"
                          onClick={() =>
                            navigate(
                              `/sensors/${sensor.id}`
                            )
                          }
                        >
                          View
                        </button>


                        <button
                          className="icon-btn icon-btn--danger"
                          aria-label={
                            `Delete ${sensor.sensor_name}`
                          }
                          onClick={() =>
                            setPendingDelete(
                              sensor
                            )
                          }
                        >

                          <Trash2 size={14} />

                        </button>

                      </div>

                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        ) : (

          <EmptyState

            title="No sensors registered yet."

            description={
              "Add your first sensor to start " +
              "receiving AI calibration " +
              "recommendations."
            }

          />

        )}

      </div>


      {/* ======================================================
          ADD SENSOR MODAL
      ====================================================== */}

      {showAdd && (

        <AddSensorModal

          onClose={() =>
            setShowAdd(false)
          }

          onCreated={() => {

            setShowAdd(false);

            refetch();

          }}

        />

      )}


      {/* ======================================================
          DELETE CONFIRMATION
      ====================================================== */}

      {pendingDelete && (

        <ConfirmDialog

          title="Delete sensor"

          message={
            `Remove ${pendingDelete.sensor_name}? ` +
            "This cannot be undone."
          }

          confirmLabel="Delete"

          onConfirm={
            handleDelete
          }

          onCancel={() =>
            setPendingDelete(null)
          }

        />

      )}

    </div>
  );
}