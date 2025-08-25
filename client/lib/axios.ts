import axios from "axios";

const baseURL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/+$/, "") ||
  "http://localhost:8000";

const axiosInstance = axios.create({
  baseURL,
  timeout: 120000,
  withCredentials: false,
  validateStatus: (s) => s >= 200 && s < 300,
});

axiosInstance.interceptors.response.use(
  (r) => r,
  (error) => {
    const msg =
      error?.response?.data?.detail ||
      error?.message ||
      "Network error. Please try again.";
    return Promise.reject(new Error(msg));
  }
);

export default axiosInstance;