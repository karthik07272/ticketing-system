// Environment configuration for frontend
export const config = {
  // API Configuration
  apiUrl: import.meta.env.VITE_API_URL || "http://localhost:8000",

  // Application Configuration
  appName: import.meta.env.VITE_APP_NAME || "Support Ticketing System",
  appVersion: import.meta.env.VITE_APP_VERSION || "1.0.0",

  // Feature Flags
  enableDebug: import.meta.env.VITE_ENABLE_DEBUG === "true",
  enableMockData: import.meta.env.VITE_ENABLE_MOCK_DATA === "true",

  // External Services
  analyticsId: import.meta.env.VITE_ANALYTICS_ID,

  // Development helpers
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD,
}

// Validate configuration
if (config.enableDebug) {
  console.log("🔧 Frontend Configuration:", config)
}

// Export individual values for convenience
export const { apiUrl, appName, appVersion, enableDebug, enableMockData, isDevelopment, isProduction } = config
