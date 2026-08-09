import { api } from "./axios";

import type {
  Sensor,
  SensorCreatePayload,
  SensorUpdatePayload,
} from "../types/sensor";

function normalizeSensor(raw: any): Sensor {
  return {
    id: Number(raw.id),
    name: raw.name ?? raw.sensor_name ?? "",
    sensor_type: raw.sensor_type ?? "",
    location: raw.location ?? "",
    status: raw.status ?? "INACTIVE",
    sensitivity:
      raw.sensitivity ?? raw.current_sensitivity ?? "MEDIUM",
    created_at: raw.created_at,
    updated_at: raw.updated_at,
    last_prediction_at: raw.last_prediction_at,
  };
}

export const sensorApi = {
  list: async (): Promise<Sensor[]> => {
    const response = await api.get("/sensors");

    const data = response.data;

    const items = Array.isArray(data)
      ? data
      : data?.items ?? data?.data ?? data?.sensors ?? [];

    return items.map(normalizeSensor);
  },

  get: async (id: number): Promise<Sensor> => {
    const response = await api.get(`/sensors/${id}`);
    return normalizeSensor(response.data);
  },

  create: async (payload: SensorCreatePayload): Promise<Sensor> => {
    const response = await api.post("/sensors", {
      sensor_name: payload.name,
      sensor_type: payload.sensor_type,
      location: payload.location,
      current_sensitivity: payload.sensitivity,
      status: payload.status ?? "ACTIVE",
    });

    return normalizeSensor(response.data);
  },

  update: async (
    id: number,
    payload: SensorUpdatePayload
  ): Promise<Sensor> => {
    const response = await api.put(`/sensors/${id}`, {
      ...(payload.name !== undefined && {
        sensor_name: payload.name,
      }),
      ...(payload.sensor_type !== undefined && {
        sensor_type: payload.sensor_type,
      }),
      ...(payload.location !== undefined && {
        location: payload.location,
      }),
      ...(payload.sensitivity !== undefined && {
        current_sensitivity: payload.sensitivity,
      }),
      ...(payload.status !== undefined && {
        status: payload.status,
      }),
    });

    return normalizeSensor(response.data);
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/sensors/${id}`);
  },

  // Keep compatibility with your existing Sensors.tsx
  remove: async (id: number): Promise<void> => {
    await api.delete(`/sensors/${id}`);
  },
};

export default sensorApi;