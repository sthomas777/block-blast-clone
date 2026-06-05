import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  // react-use-websocket is a CommonJS package. Pre-bundling it at startup
  // ensures Vite applies CJS->ESM interop up front, rather than discovering
  // it mid-session (which can serve a non-interop'd module and break the
  // default import: "useWebSocket is not a function").
  optimizeDeps: {
    include: ["react-use-websocket"],
  },
});
