import axios from "axios";

export const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_BASE_URL ||
    "http://127.0.0.1:8000/api/v1",

  headers: {
    "Content-Type": "application/json",
  },

  timeout: 15000,
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error(
      "[API ERROR]",
      error?.config?.url,
      error?.response?.status,
      error?.message
    );

    return Promise.reject(error);
  }
);

export default api;