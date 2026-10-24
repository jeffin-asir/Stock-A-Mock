const express = require('express');
const cors = require('cors');
const oracledb = require('oracledb');
const dotenv = require('dotenv');
require('dotenv').config();
// Local mini-project fallbacks; environment variables take precedence.
process.env.DB_USER ||= "Stock";
process.env.DB_PASSWORD ||= "StockMock";
process.env.JWT_SECRET ||= "ithinkthatkidmightbetheavatar";

const app = express();
const db = require('./connection/db'); // Import your DB module
const port = 5001;

const defaultOrigins = [
  "http://localhost:5173",
  "http://localhost:3000",
  "http://localhost:8080",
  "http://10.7.103.226:5173",
  "http://10.5.12.254:5173",
  "http://192.168.1.200:5173",
  "http://10.21.68.19:5173"
];

const allowedOrigins = process.env.CORS_ORIGINS
  ? process.env.CORS_ORIGINS.split(",").map((origin) => origin.trim())
  : defaultOrigins;

const isPrivateIPv4 = (hostname) => {
  const octets = hostname.split(".").map(Number);
  if (octets.length !== 4 || octets.some((octet) => !Number.isInteger(octet) || octet < 0 || octet > 255)) {
    return false;
  }

  return octets[0] === 10 ||
    (octets[0] === 172 && octets[1] >= 16 && octets[1] <= 31) ||
    (octets[0] === 192 && octets[1] === 168);
};

const isLocalDevelopmentOrigin = (origin) => {
  if (!origin) return false;

  try {
    const { hostname, protocol } = new URL(origin);
    const isHttpOrigin = ["http:", "https:"].includes(protocol);
    const isLoopback = ["localhost", "127.0.0.1", "[::1]"].includes(hostname);
    const isPrivateNetwork = process.env.NODE_ENV !== "production" &&
      (isPrivateIPv4(hostname) || hostname.endsWith(".local"));

    return isHttpOrigin && (isLoopback || isPrivateNetwork);
  } catch {
    return false;
  }
};

app.use(cors({
  origin: (origin, callback) => {
    if (!origin || allowedOrigins.includes(origin) || isLocalDevelopmentOrigin(origin)) {
      callback(null, true);
    }
    else callback(new Error("Not allowed by CORS."));
  },
  credentials: true,
}));

app.use(express.json());

const userRoutes = require('./routes/user');
const mailRoutes = require('./routes/mail');
const dematRoutes = require('./routes/demat');
const stockRoutes = require('./routes/stock');
const transactionRoutes = require('./routes/transaction');
const portfolioRoutes = require('./routes/portfolio'); 

require('./jobs/stockUpdater');

app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'stock-a-mock-backend' });
});

app.use('/api/user', userRoutes);
app.use('/api/mail', mailRoutes);
app.use('/api/demat', dematRoutes);
app.use('/api/stock', stockRoutes);
app.use('/api/transaction', transactionRoutes);
app.use('/api/portfolio', portfolioRoutes); 

// Startup
(async () => {
  await db.initPool();
})();

app.listen(port, '0.0.0.0', () => {
  console.log(`🚀 Server running at http://localhost:${port}`);
});

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log("📴 Gracefully shutting down...");
  try {
    await oracledb.getPool().close(0);
    console.log("🧹 Oracle connection pool closed.");
  } catch (err) {
    console.error("Error closing Oracle pool:", err);
  }
  process.exit(0);
});
