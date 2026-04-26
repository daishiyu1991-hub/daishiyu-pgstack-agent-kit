#!/usr/bin/env node
import { readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const DEFAULT_URL = "http://8.129.13.96:8480/gbrain/mcp";

function arg(name) {
  const idx = process.argv.indexOf(name);
  if (idx < 0) return "";
  return process.argv[idx + 1] || "";
}

function has(flag) {
  return process.argv.includes(flag);
}

function readToken() {
  if (process.env.PGSTACK_GBRAIN_REMOTE_MCP_TOKEN) {
    return process.env.PGSTACK_GBRAIN_REMOTE_MCP_TOKEN.trim();
  }
  const file =
    process.env.PGSTACK_GBRAIN_REMOTE_MCP_TOKEN_FILE ||
    join(homedir(), ".codex", "secrets", "pgstack_gbrain_remote_mcp_token");
  try {
    return readFileSync(file, "utf8").trim();
  } catch {
    return "";
  }
}

async function rpc(url, token, method, params, id) {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${token}`,
      accept: "application/json, text/event-stream",
    },
    body: JSON.stringify({ jsonrpc: "2.0", method, params, id }),
  });
  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    throw new Error(`${method} returned non-json status=${res.status}: ${text.slice(0, 160)}`);
  }
  if (!res.ok || data.error) {
    throw new Error(`${method} failed status=${res.status}: ${JSON.stringify(data.error || data)}`);
  }
  return data.result;
}

async function run() {
  const url = arg("--url") || process.env.PGSTACK_GBRAIN_REMOTE_MCP_URL || DEFAULT_URL;
  const requireConfig = has("--require-config");
  const writeSmoke = has("--write-smoke");
  const jsonOutput = has("--json");
  const token = readToken();
  if (!token) {
    const result = {
      check: "gbrain_remote_mcp_health",
      verdict: requireConfig ? "FAIL" : "SKIP",
      missing: ["PGSTACK_GBRAIN_REMOTE_MCP_TOKEN or token file"],
      url,
    };
    return finish(result, jsonOutput);
  }

  const checks = [];
  const result = {
    check: "gbrain_remote_mcp_health",
    verdict: "PASS",
    url,
    checks,
  };

  try {
    const init = await rpc(url, token, "initialize", {
      protocolVersion: "2025-03-26",
      capabilities: {},
      clientInfo: { name: "pgstack-gbrain-remote-mcp-health", version: "1.0" },
    }, 1);
    checks.push({ name: "initialize", passed: init?.serverInfo?.name === "gbrain-remote-mcp" });

    const tools = await rpc(url, token, "tools/list", {}, 2);
    checks.push({ name: "tools/list", passed: Array.isArray(tools?.tools), count: tools?.tools?.length || 0 });

    const stats = await rpc(url, token, "tools/call", { name: "get_stats", arguments: {} }, 3);
    const statsPayload = JSON.parse(stats.content[0].text);
    checks.push({
      name: "get_stats",
      passed: Number.isFinite(statsPayload.page_count),
      page_count: statsPayload.page_count,
      chunk_count: statsPayload.chunk_count,
    });

    if (writeSmoke) {
      const slug = "reports/gbrain-remote-mcp-health-latest";
      const now = new Date().toISOString();
      const content = `---\ntitle: GBrain Remote MCP Health Latest\ntype: report\nstatus: active\nupdated: ${now}\n---\n\n# GBrain Remote MCP Health Latest\n\nWrite smoke passed via the formal Remote MCP route.\n\n- checked_at: ${now}\n- route: ${url}\n`;
      const put = await rpc(url, token, "tools/call", { name: "put_page", arguments: { slug, content } }, 4);
      const putPayload = JSON.parse(put.content[0].text);
      checks.push({ name: "put_page", passed: putPayload.slug === slug, slug });
      const get = await rpc(url, token, "tools/call", { name: "get_page", arguments: { slug } }, 5);
      const getPayload = JSON.parse(get.content[0].text);
      checks.push({ name: "get_page", passed: getPayload.slug === slug, slug });
    }

    if (checks.some((check) => !check.passed)) {
      result.verdict = "FAIL";
    }
  } catch (error) {
    result.verdict = "FAIL";
    result.error = error instanceof Error ? error.message : String(error);
  }

  return finish(result, jsonOutput);
}

function finish(result, jsonOutput) {
  if (jsonOutput) {
    console.log(JSON.stringify(result));
  } else {
    console.log(`gbrain-remote-mcp health: ${result.verdict}`);
    console.log(`url: ${result.url}`);
    for (const check of result.checks || []) {
      const details = Object.entries(check)
        .filter(([key]) => !["name", "passed"].includes(key))
        .map(([key, value]) => `${key}=${value}`)
        .join(" ");
      console.log(`  ${check.passed ? "PASS" : "FAIL"} ${check.name}${details ? ` ${details}` : ""}`);
    }
    if (result.error) console.log(`error: ${result.error}`);
    if (result.missing) {
      for (const item of result.missing) console.log(`missing: ${item}`);
    }
  }
  return result.verdict === "PASS" || result.verdict === "SKIP" ? 0 : 2;
}

run().then((code) => process.exit(code));
