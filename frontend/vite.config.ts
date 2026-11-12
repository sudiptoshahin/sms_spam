import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In dev, requests to /predict are forwarded to your Flask server.
export default defineConfig({
  plugins: [react()],
  server: { proxy: { "/predict": "http://localhost:5000" } },
});
