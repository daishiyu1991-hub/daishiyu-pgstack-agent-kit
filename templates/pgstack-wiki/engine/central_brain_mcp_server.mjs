#!/usr/bin/env node
/**
 * Central GBrain MCP bridge for Codex.
 *
 * This server is intentionally thin: it exposes MCP tools that call the
 * already-accepted `central_brain_lookup.py` adapter. It does not start a
 * competing gbrain server on the cloud host, mutate MemTensor, or write brain
 * pages. The cloud Central Brain Host remains the source of truth.
 */

import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const require = createRequire(import.meta.url);

async function importModule(packageName, envPath) {
  if (process.env[envPath]) {
    return import(pathToFileURL(process.env[envPath]).href);
  }
  try {
    return await import(packageName);
  } catch (error) {
    const resolved = require.resolve(packageName);
    return import(pathToFileURL(resolved).href);
  }
}

const { McpServer } = await importModule("@modelcontextprotocol/sdk/server/mcp.js", "PGSTACK_MCP_SERVER_ENTRY");
const { StdioServerTransport } = await importModule(
  "@modelcontextprotocol/sdk/server/stdio.js",
  "PGSTACK_MCP_STDIO_ENTRY",
);
const { z } = await importModule("zod", "PGSTACK_ZOD_ENTRY");

const LOOKUP_SCRIPT =
  process.env.PGSTACK_CENTRAL_BRAIN_LOOKUP ||
  resolve(__dirname, "central_brain_lookup.py");
const PYTHON = process.env.PGSTACK_PYTHON || "python3";
const DEFAULT_MEMORY_OWNER = process.env.PGSTACK_CENTRAL_BRAIN_MEMORY_OWNER || "central";
const DEFAULT_TIMEOUT_SECONDS = Number(process.env.PGSTACK_CENTRAL_BRAIN_TIMEOUT || "30");

function asText(value) {
  return {
    content: [
      {
        type: "text",
        text: typeof value === "string" ? value : JSON.stringify(value, null, 2),
      },
    ],
  };
}

function buildBaseArgs(command, params) {
  const args = [LOOKUP_SCRIPT, command];
  if (command === "lookup") {
    args.push("--query", params.query);
  }
  args.push("--memory-owner", params.memoryOwner || DEFAULT_MEMORY_OWNER);
  args.push("--max-results", String(params.maxResults ?? 6));
  args.push("--min-score", String(params.minScore ?? 0));
  args.push("--timeout", String(params.timeoutSeconds ?? DEFAULT_TIMEOUT_SECONDS));
  if (params.noMemory) args.push("--no-memory");
  if (params.noBrain) args.push("--no-brain");
  if (params.smokeMarker) args.push("--smoke-marker", params.smokeMarker);
  return args;
}

function runJson(command, params) {
  const args = buildBaseArgs(command, params);
  const timeoutSeconds = params.timeoutSeconds ?? DEFAULT_TIMEOUT_SECONDS;
  const hardTimeoutMs = Math.max(10_000, timeoutSeconds * 1000 + 5_000);

  return new Promise((resolvePromise, reject) => {
    const child = spawn(PYTHON, args, {
      cwd: resolve(__dirname, ".."),
      env: process.env,
      stdio: ["ignore", "pipe", "pipe"],
    });

    let stdout = "";
    let stderr = "";
    let settled = false;

    const timer = setTimeout(() => {
      if (settled) return;
      settled = true;
      child.kill("SIGTERM");
      reject(new Error(`central brain ${command} timed out after ${hardTimeoutMs}ms`));
    }, hardTimeoutMs);

    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString("utf8");
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString("utf8");
    });
    child.on("error", (error) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      reject(error);
    });
    child.on("close", (code) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      const trimmed = stdout.trim();
      if (!trimmed) {
        reject(new Error(`central brain ${command} produced no JSON output: ${stderr.slice(-1200)}`));
        return;
      }
      try {
        const parsed = JSON.parse(trimmed);
        parsed.mcp_bridge = {
          name: "central-gbrain-mcp-bridge",
          exit_code: code,
          read_only: true,
        };
        if (stderr.trim()) {
          parsed.mcp_bridge.stderr_preview = stderr.trim().slice(-1200);
        }
        resolvePromise(parsed);
      } catch (error) {
        reject(
          new Error(
            `central brain ${command} returned non-JSON output: ${trimmed.slice(0, 1200)} ${stderr.slice(-1200)}`,
          ),
        );
      }
    });
  });
}

function statusPayload() {
  const sshKey = process.env.PGSTACK_CENTRAL_BRAIN_SSH_KEY || "";
  return {
    bridge: "central-gbrain-mcp-bridge",
    stage: "stage3.2-codex-central-gbrain-mcp-bridge",
    read_only: true,
    lookup_script: LOOKUP_SCRIPT,
    lookup_script_exists: existsSync(LOOKUP_SCRIPT),
    python: PYTHON,
    mcp_imports: {
      server_entry: process.env.PGSTACK_MCP_SERVER_ENTRY || "@modelcontextprotocol/sdk/server/mcp.js",
      stdio_entry: process.env.PGSTACK_MCP_STDIO_ENTRY || "@modelcontextprotocol/sdk/server/stdio.js",
      zod_entry: process.env.PGSTACK_ZOD_ENTRY || "zod",
    },
    configured: {
      ssh_target_present: Boolean(process.env.PGSTACK_CENTRAL_BRAIN_SSH_TARGET),
      ssh_key_present: Boolean(sshKey),
      ssh_key_exists: sshKey ? existsSync(sshKey) : false,
      default_memory_owner: DEFAULT_MEMORY_OWNER,
      timeout_seconds: DEFAULT_TIMEOUT_SECONDS,
    },
    boundaries: [
      "does not start cloud gbrain serve",
      "does not write MemTensor",
      "does not publish team_shared",
      "does not mutate cloud brain pages",
    ],
  };
}

const server = new McpServer({
  name: "central-gbrain-mcp-bridge",
  version: "0.1.0",
});

server.tool(
  "central_brain_lookup",
  "Read-only lookup against the ECS Central Brain Host: cloud GBrain first, MemTensor memory_context fallback second.",
  {
    query: z.string().min(1).describe("Question or search query for the central brain."),
    memoryOwner: z
      .enum(["central", "cloud", "hermes-admin", "hermes"])
      .default(DEFAULT_MEMORY_OWNER)
      .describe("Owner route. Aliases central/cloud/hermes-admin resolve to hermes."),
    maxResults: z.number().int().min(1).max(20).default(6),
    minScore: z.number().min(0).max(1).default(0),
    timeoutSeconds: z.number().int().min(5).max(120).default(DEFAULT_TIMEOUT_SECONDS),
    noMemory: z.boolean().default(false).describe("Skip MemTensor fallback."),
    noBrain: z.boolean().default(false).describe("Skip GBrain lookup."),
  },
  async (params) => asText(await runJson("lookup", params)),
);

server.tool(
  "central_brain_smoke",
  "Run the accepted read-only central brain smoke test from Codex through the MCP bridge.",
  {
    memoryOwner: z
      .enum(["central", "cloud", "hermes-admin", "hermes"])
      .default(DEFAULT_MEMORY_OWNER)
      .describe("Owner route. Aliases central/cloud/hermes-admin resolve to hermes."),
    maxResults: z.number().int().min(1).max(20).default(6),
    minScore: z.number().min(0).max(1).default(0),
    timeoutSeconds: z.number().int().min(5).max(120).default(DEFAULT_TIMEOUT_SECONDS),
    smokeMarker: z.string().optional().describe("Override the default write-through acceptance marker."),
  },
  async (params) => asText(await runJson("smoke", params)),
);

server.tool(
  "central_brain_status",
  "Return local configuration and boundary status for the Central GBrain MCP bridge.",
  {},
  async () => asText(statusPayload()),
);

const transport = new StdioServerTransport();
await server.connect(transport);
