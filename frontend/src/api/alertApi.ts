import { api } from "./axios";
import type { Alert } from "../types/alert";

export const alertApi = {
  list: () => api.get<Alert[]>("/alerts").then((r) => r.data),
  get: (id: number | string) => api.get<Alert>(`/alerts/${id}`).then((r) => r.data),
  deactivate: (id: number | string) =>
    api.delete(`/alerts/${id}`).then((r) => r.data),
};
