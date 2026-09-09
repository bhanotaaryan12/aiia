import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

const api = axios.create({ baseURL: API_URL, headers: { "Content-Type": "application/json" }, withCredentials: true });

function csrfToken() {
  if (typeof document === "undefined") return undefined;
  return document.cookie.split("; ").find((item) => item.startsWith("csrf_token="))?.split("=")[1];
}

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    if (["post", "put", "patch", "delete"].includes(config.method || "")) {
      const token = csrfToken();
      if (token) config.headers["X-CSRF-Token"] = token;
    }
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

export default api;

export async function login(email: string, password: string) {
  await api.post("/auth/login", { email, password });
  const me = await api.get("/auth/me");
  localStorage.setItem("user", JSON.stringify(me.data));
  return me.data;
}

export async function logout() {
  try {
    await api.post("/auth/logout");
  } finally {
    localStorage.removeItem("user");
    window.location.href = "/login";
  }
}

export function clearSession() {
  localStorage.removeItem("user");
}

export function getUser() {
  if (typeof window === "undefined") return null;
  const u = localStorage.getItem("user");
  return u ? JSON.parse(u) : null;
}

export function isAuthenticated() {
  if (typeof window === "undefined") return false;
  return !!localStorage.getItem("user");
}
