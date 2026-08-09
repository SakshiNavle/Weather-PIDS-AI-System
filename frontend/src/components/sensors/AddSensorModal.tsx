import { useState } from "react";
import { Modal } from "../common/Modal";
import { sensorApi } from "../../api/sensorApi";
import { useToast } from "../common/ToastContext";
import type { SensorCreatePayload } from "../../types/sensor";

interface AddSensorModalProps {
  onClose: () => void;
  onCreated: () => void;
}

const SENSOR_TYPES = ["Temperature", "Motion", "Vibration", "Infrared", "Microwave", "Acoustic"];
const SENSITIVITIES = ["LOW", "MEDIUM", "HIGH"] as const;

export function AddSensorModal({ onClose, onCreated }: AddSensorModalProps) {
  const { showToast } = useToast();
  const [form, setForm] = useState<SensorCreatePayload>({
    name: "",
    sensor_type: SENSOR_TYPES[0],
    location: "",
    sensitivity: "MEDIUM",
    status: "ACTIVE",
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitting, setSubmitting] = useState(false);

  const validate = () => {
    const next: Record<string, string> = {};
    if (!form.name.trim()) next.name = "Sensor name is required.";
    if (!form.location.trim()) next.location = "Location is required.";
    if (!form.sensor_type) next.sensor_type = "Sensor type is required.";
    if (!form.sensitivity) next.sensitivity = "Sensitivity is required.";
    setErrors(next);
    return Object.keys(next).length === 0;
  };

  const handleSubmit = async () => {
    if (!validate()) return;
    setSubmitting(true);
    try {
      await sensorApi.create(form);
      showToast("Sensor created successfully", "success");
      onCreated();
      onClose();
    } catch (err) {
      const message = err instanceof Error ? err.message : "Could not create sensor.";
      showToast(message, "error");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Modal
      title="Add Sensor"
      onClose={onClose}
      footer={
        <>
          <button className="btn btn--ghost" onClick={onClose} disabled={submitting}>
            Cancel
          </button>
          <button className="btn btn--primary" onClick={handleSubmit} disabled={submitting}>
            {submitting ? "Creating..." : "Create Sensor"}
          </button>
        </>
      }
    >
      <div className="field">
        <label htmlFor="sensor-name">Sensor Name</label>
        <input
          id="sensor-name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          placeholder="Temperature Sensor 01"
        />
        {errors.name && <span className="field__error">{errors.name}</span>}
      </div>

      <div className="field">
        <label htmlFor="sensor-type">Sensor Type</label>
        <select
          id="sensor-type"
          value={form.sensor_type}
          onChange={(e) => setForm({ ...form, sensor_type: e.target.value })}
        >
          {SENSOR_TYPES.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
        {errors.sensor_type && <span className="field__error">{errors.sensor_type}</span>}
      </div>

      <div className="field">
        <label htmlFor="sensor-location">Location</label>
        <input
          id="sensor-location"
          value={form.location}
          onChange={(e) => setForm({ ...form, location: e.target.value })}
          placeholder="Pune"
        />
        {errors.location && <span className="field__error">{errors.location}</span>}
      </div>

      <div className="field">
        <label htmlFor="sensor-sensitivity">Initial Sensitivity</label>
        <select
          id="sensor-sensitivity"
          value={form.sensitivity}
          onChange={(e) => setForm({ ...form, sensitivity: e.target.value as SensorCreatePayload["sensitivity"] })}
        >
          {SENSITIVITIES.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        {errors.sensitivity && <span className="field__error">{errors.sensitivity}</span>}
      </div>

      <div className="field">
        <label htmlFor="sensor-status">Status</label>
        <select
          id="sensor-status"
          value={form.status}
          onChange={(e) => setForm({ ...form, status: e.target.value as SensorCreatePayload["status"] })}
        >
          <option value="ACTIVE">ACTIVE</option>
          <option value="INACTIVE">INACTIVE</option>
        </select>
      </div>
    </Modal>
  );
}
