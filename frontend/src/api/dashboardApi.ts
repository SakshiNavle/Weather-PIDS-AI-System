import { api } from "./axios";
import type { DashboardData } from "../types/dashboard";

export const dashboardApi = {
  getDashboard: async (): Promise<DashboardData> => {
    const response = await api.get<DashboardData>("/dashboard");
    return response.data;
  },
};

export default dashboardApi;