const http = require("http");

const PORT = process.env.PORT || 5001;

const stocks = [
  [1, "AAPL", "Technology", 189.42, "2026-01-01"],
  [2, "MSFT", "Technology", 412.18, "2026-01-01"],
  [3, "TSLA", "Automotive", 248.7, "2026-01-01"],
  [4, "JPM", "Finance", 198.11, "2026-01-01"],
];

function sendJson(res, status, body) {
  const payload = JSON.stringify(body);
  res.writeHead(status, {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  });
  res.end(payload);
}

const server = http.createServer((req, res) => {
  if (req.method === "OPTIONS") {
    sendJson(res, 204, {});
    return;
  }

  const url = req.url.split("?")[0];

  if (url === "/health") {
    sendJson(res, 200, { status: "ok", service: "mock-api" });
    return;
  }

  if (url === "/api/stock") {
    sendJson(res, 200, { stocks });
    return;
  }

  if (url === "/api/portfolio") {
    sendJson(res, 200, { holdings: [] });
    return;
  }

  sendJson(res, 404, { error: "Not found" });
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`Mock API listening on ${PORT}`);
});
