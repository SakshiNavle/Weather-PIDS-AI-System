import { api } from "./axios";
import type { Sensor, SensorCreatePayload, SensorUpdatePayload } from "../types/sensor";

export const sensorApi = {
  list: () => api.get<Sensor[]>("/sensors").then((r) => r.data),
  get: (id: number | string) => api.get<Sensor>(`/sensors/${id}`).then((r) => r.data),
  create: (payload: SensorCreatePayload) =>
    api.post<Sensor>("/sensors", payload).then((r) => r.data),
  update: (id: number | string, payload: SensorUpdatePayload) =>
    api.put<Sensor>(`/sensors/${id}`, payload).then((r) => r.data),
  remove: (id: number | string) => api.delete(`/sensors/${id}`).then((r) => r.data),
};
