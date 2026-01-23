import type { NextConfig } from "next";
const withPWA = require("next-pwa")({
  dest: "public",
  register: true,
  skipWaiting: true,
  disable: false, // Temporarily enable for testing
  runtimeCaching: [],
});

const nextConfig: NextConfig = {
  reactStrictMode: false,
};

export default withPWA(nextConfig);
