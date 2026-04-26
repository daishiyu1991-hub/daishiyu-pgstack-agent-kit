#!/usr/bin/env node
import { spawn } from "node:child_process";
import { createServer } from "node:http";
import { readFileSync } from "node:fs";

const HOST = process.env.GBRAIN_REMOTE_MCP_HOST || "127.0.0.1";
const PORT = Number(process.env.GBRAIN_REMOTE_MCP_PORT || "8787");
const CONTAINER = process.env.GBRAIN_REMOTE_MCP_CONTAINER || "hermes-admin";
const TOKEN = readToken();
const MAX_BODY_BYTES = Number(process.env.GBRAIN_REMOTE_MCP_MAX_BODY_BYTES || 10 * 1024 * 1024);
const COMMAND_TIMEOUT_MS = Number(process.env.GBRAIN_REMOTE_MCP_COMMAND_TIMEOUT_MS || 120_000);

function readToken() {
  if (process.env.GBRAIN_REMOTE_MCP_TOKEN) return process.env.GBRAIN_REMOTE_MCP_TOKEN.trim();
  const file = process.env.GBRAIN_REMOTE_MCP_TOKEN_FILE;
  if (!file) return "";
  return readFileSync(file, "utf8").trim();
}

function json(res, status, body) {
  res.writeHead(status, {
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store",
  });
  res.end(JSON.stringify(body));
}

function unauthorized(res) {
  json(res, 401, {
    jsonrpc: "2.0",
    error: { code: -32001, message: "missing_or_invalid_bearer_token" },
    id: null,
  });
}

function requireAuth(req, res) {
  if (!TOKEN) {
    json(res, 503, {
      jsonrpc: "2.0",
      error: { code: -32002, message: "server_token_not_configured" },
      id: null,
    });
    return false;
  }
  const expected = `Bearer ${TOKEN}`;
  if (req.headers.authorization !== expected) {
    unauthorized(res);
    return false;
  }
  return true;
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    req.on("data", (chunk) => {
      size += chunk.length;
      if (size > MAX_BODY_BYTES) {
        reject(new Error("request_body_too_large"));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    req.on("error", reject);
  });
}

function runGbrain(args) {
  return new Promise((resolve, reject) => {
    const child = spawn("docker", [
      "exec",
      "-e",
      "HOME=/opt/data",
      CONTAINER,
      "sh",
      "-lc",
      "cd /opt/data/gbrain && exec /opt/data/.bun/bin/bun run src/cli.ts \"$@\"",
      "gbrain-remote-mcp",
      ...args,
    ], {
      stdio: ["ignore", "pipe", "pipe"],
    });

    let stdout = "";
    let stderr = "";
    const timer = setTimeout(() => {
      child.kill("SIGTERM");
      reject(new Error(`gbrain_command_timeout_after_${COMMAND_TIMEOUT_MS}ms`));
    }, COMMAND_TIMEOUT_MS);

    child.stdout.on("data", (chunk) => { stdout += chunk.toString(); });
    child.stderr.on("data", (chunk) => { stderr += chunk.toString(); });
    child.on("error", (err) => {
      clearTimeout(timer);
      reject(err);
    });
    child.on("close", (code) => {
      clearTimeout(timer);
      if (code === 0) {
        resolve(stdout.trim());
      } else {
        reject(new Error((stderr || stdout || `gbrain exited ${code}`).trim()));
      }
    });
  });
}

function parseJsonOutput(text) {
  if (!text) return null;
  return JSON.parse(text);
}

function toJsonSchema(parameters = {}) {
  const properties = {};
  const required = [];
  for (const [name, raw] of Object.entries(parameters)) {
    const spec = String(raw);
    const optional = spec.endsWith("?");
    const base = optional ? spec.slice(0, -1) : spec;
    properties[name] = schemaForType(base);
    if (!optional) required.push(name);
  }
  return {
    type: "object",
    properties,
    required,
    additionalProperties: false,
  };
}

function schemaForType(type) {
  if (type === "string") return { type: "string" };
  if (type === "number") return { type: "number" };
  if (type === "boolean") return { type: "boolean" };
  if (type === "object") return { type: "object" };
  if (type === "array") return { type: "array" };
  return { type: ["string", "number", "boolean", "object", "array", "null"] };
}

async function listTools() {
  const raw = await runGbrain(["--tools-json"]);
  const tools = parseJsonOutput(raw);
  return tools.map((tool) => ({
    name: tool.name,
    description: tool.description || "",
    inputSchema: toJsonSchema(tool.parameters || {}),
  }));
}

async function callTool(name, args) {
  if (!name || typeof name !== "string") {
    throw new Error("tools/call requires params.name");
  }
  const raw = await runGbrain(["call", name, JSON.stringify(args || {})]);
  return parseJsonOutput(raw);
}

function ok(id, result) {
  return { jsonrpc: "2.0", id, result };
}

function fail(id, code, message) {
  return { jsonrpc: "2.0", id: id ?? null, error: { code, message } };
}

async function handleRpc(request) {
  const id = request.id;
  const method = request.method;
  if (method === "initialize") {
    return ok(id, {
      protocolVersion: request.params?.protocolVersion || "2025-03-26",
      capabilities: { tools: {} },
      serverInfo: { name: "gbrain-remote-mcp", version: "1.0.0" },
    });
  }
  if (method === "ping") {
    return ok(id, {});
  }
  if (method === "tools/list") {
    return ok(id, { tools: await listTools() });
  }
  if (method === "tools/call") {
    const result = await callTool(request.params?.name, request.params?.arguments || {});
    return ok(id, {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
    });
  }
  if (method?.startsWith("notifications/")) {
    return null;
  }
  return fail(id, -32601, `method_not_found: ${method}`);
}

const server = createServer(async (req, res) => {
  try {
    if (req.method === "GET" && req.url === "/healthz") {
      json(res, 200, { ok: true, name: "gbrain-remote-mcp" });
      return;
    }
    if (req.method !== "POST" || req.url !== "/mcp") {
      json(res, 404, { error: "not_found" });
      return;
    }
    if (!requireAuth(req, res)) return;

    const body = await readBody(req);
    const request = JSON.parse(body || "{}");
    const response = await handleRpc(request);
    if (response === null) {
      res.writeHead(204);
      res.end();
      return;
    }
    json(res, 200, response);
  } catch (err) {
    json(res, 500, fail(null, -32603, err instanceof Error ? err.message : String(err)));
  }
});

server.listen(PORT, HOST, () => {
  process.stdout.write(`gbrain-remote-mcp listening on ${HOST}:${PORT}\n`);
});
