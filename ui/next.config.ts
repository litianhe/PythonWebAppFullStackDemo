import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  output: 'export',
  distDir: "../backend/static",
  assetPrefix: '/static',
  experimental: {
    reactCompiler: false,
  }
};

export default nextConfig;
