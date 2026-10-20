const configuredApiBase = import.meta.env.VITE_API_URL?.trim();
const apiHost = window.location.hostname;

// Use the machine serving the frontend so LAN clients don't call their own localhost.
export const API_BASE = configuredApiBase || `${window.location.protocol}//${apiHost}:5001`;
