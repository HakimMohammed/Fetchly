export const APP_CONFIG = {
    name: process.env.NEXT_PUBLIC_APP_NAME || "Fetchly",
    version: process.env.NEXT_PUBLIC_APP_VERSION || "0.1.0",
    apiUrl: process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000",
} as const;
