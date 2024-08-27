import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  root: path.join(__dirname, "./modules_source"),
  base: "/assets/",
  build: {
    outDir: path.join(__dirname, "./assets_compiled/"),
    manifest: "manifest.json",
    assetsDir: "bundled",
    rollupOptions: {
      input: [
        "modules_source/auth/auth-main.jsx",
        "modules_source/profile/profile-main.jsx",
      ],
    },
    emptyOutDir: true,
    copyPublicDir: false,
  },
});
