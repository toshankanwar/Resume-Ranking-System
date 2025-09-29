/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    // Ensure React 19 compatibility
    experimental: {
      ppr: false,
    },
    // Force CSS processing
    compiler: {
      // Enable SWC CSS processing
      styledComponents: true,
    },
    webpack: (config, { dev, isServer }) => {
      // Ensure CSS is processed correctly
      if (!dev && !isServer) {
        config.resolve.fallback = {
          ...config.resolve.fallback,
          fs: false,
        }
      }
      return config
    }
  }
  
  export default nextConfig
  