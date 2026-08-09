import { api } from "./axios";
import type { Prediction, RunAllResult } from "../types/prediction";

export const predictionApi = {
  list: () => api.get<Prediction[]>("/predictions").then((r) => r.data),
  bySensor: (sensorId: number | string) =>
    api.get<Prediction[]>(`/predictions/sensor/${sensorId}`).then((r) => r.data),
  run: (sensorId: number | string) =>
    api.post<Prediction>(`/predictions/run`, null, { params: { sensor_id: sensorId } }).then((r) => r.data),
  runAll: () => api.post<RunAllResult>("/predictions/run-all").then((r) => r.data),
};
