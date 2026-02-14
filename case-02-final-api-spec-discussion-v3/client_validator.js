#!/usr/bin/env node

/**
 * client_validator.js
 *
 * Fetches from the mock server and validates the response against
 * all HC-F constraints from the API contract.
 *
 * Usage: node client_validator.js
 * Requires: Node.js 18+ (uses native fetch)
 */

const BASE_URL = "http://localhost:8080/dashboard/orders";
const MAX_PAYLOAD_BYTES = 50 * 1024; // 50KB budget (HC-F4)

const VALID_STATUSES = ["pending", "confirmed", "shipped", "delivered", "cancelled"];

let passCount = 0;
let failCount = 0;

function pass(check) {
  passCount++;
  console.log(`  PASS: ${check}`);
}

function fail(check, detail) {
  failCount++;
  console.log(`  FAIL: ${check}`);
  if (detail) console.log(`        ${detail}`);
}

async function main() {
  console.log("=== Client Validator: HC-F Constraint Checks ===\n");

  // -------------------------------------------------------
  // HC-F1: Single HTTP request for above-the-fold content
  // -------------------------------------------------------
  console.log("[HC-F1] Single HTTP request for above-the-fold content");

  let res;
  let bodyText;
  let requestCount = 0;

  try {
    requestCount++;
    res = await fetch(BASE_URL);
    bodyText = await res.text();
  } catch (err) {
    fail("Fetch from mock server", `Could not connect: ${err.message}`);
    console.log(`\n=== RESULT: ${passCount} passed, ${failCount} failed ===`);
    process.exit(1);
  }

  if (res.status === 200) {
    pass(`Single request returned HTTP ${res.status}`);
  } else {
    fail(`Expected HTTP 200`, `Got ${res.status}`);
  }

  if (requestCount === 1) {
    pass("Above-the-fold data retrieved in exactly 1 HTTP request");
  } else {
    fail("Above-the-fold data required more than 1 HTTP request");
  }

  // -------------------------------------------------------
  // HC-F4: Payload size < 50KB
  // -------------------------------------------------------
  console.log("\n[HC-F4] Payload size < 50KB for 4G networks");

  const payloadBytes = Buffer.byteLength(bodyText, "utf-8");
  const payloadKB = (payloadBytes / 1024).toFixed(2);

  if (payloadBytes < MAX_PAYLOAD_BYTES) {
    pass(`Payload size: ${payloadKB} KB (under 50KB limit)`);
  } else {
    fail(`Payload size: ${payloadKB} KB`, `Exceeds 50KB limit`);
  }

  // -------------------------------------------------------
  // Parse JSON
  // -------------------------------------------------------
  let data;
  try {
    data = JSON.parse(bodyText);
  } catch (err) {
    fail("JSON parse", `Invalid JSON: ${err.message}`);
    console.log(`\n=== RESULT: ${passCount} passed, ${failCount} failed ===`);
    process.exit(1);
  }

  // -------------------------------------------------------
  // HC-F3: Response contains all data needed for order cards
  // -------------------------------------------------------
  console.log("\n[HC-F3] Response contains all data for order card rendering");

  // Top-level structure
  if (data.orders && Array.isArray(data.orders)) {
    pass(`"orders" is an array with ${data.orders.length} items`);
  } else {
    fail(`"orders" field missing or not an array`);
    console.log(`\n=== RESULT: ${passCount} passed, ${failCount} failed ===`);
    process.exit(1);
  }

  if (data.pagination && typeof data.pagination === "object") {
    pass(`"pagination" object present`);
  } else {
    fail(`"pagination" field missing or not an object`);
  }

  // Pagination fields
  const pag = data.pagination || {};
  for (const field of ["limit", "offset", "total"]) {
    if (typeof pag[field] === "number") {
      pass(`pagination.${field} = ${pag[field]}`);
    } else {
      fail(`pagination.${field} missing or not a number`);
    }
  }

  // Validate each order
  const orderFields = ["id", "status", "total_cents", "currency", "created_at", "items"];

  for (let i = 0; i < data.orders.length; i++) {
    const order = data.orders[i];
    console.log(`\n  --- Order ${i + 1}: ${order.id || "(no id)"} ---`);

    // Required order fields
    for (const field of orderFields) {
      if (order[field] !== undefined && order[field] !== null) {
        pass(`order.${field} present`);
      } else {
        fail(`order.${field} missing`);
      }
    }

    // Status enum
    if (VALID_STATUSES.includes(order.status)) {
      pass(`order.status "${order.status}" is a valid enum value`);
    } else {
      fail(`order.status "${order.status}" not in enum`, `Expected one of: ${VALID_STATUSES.join(", ")}`);
    }

    // total_cents is integer
    if (Number.isInteger(order.total_cents)) {
      pass(`order.total_cents is integer (${order.total_cents})`);
    } else {
      fail(`order.total_cents is not an integer`);
    }

    // created_at is ISO 8601
    if (order.created_at && !isNaN(Date.parse(order.created_at))) {
      pass(`order.created_at is valid ISO 8601`);
    } else {
      fail(`order.created_at is not valid ISO 8601`);
    }

    // Items array
    if (!Array.isArray(order.items) || order.items.length === 0) {
      fail(`order.items missing or empty`);
      continue;
    }

    pass(`order.items has ${order.items.length} item(s)`);

    // Validate each item — HC-F2 and HC-F3 checks
    const itemFields = ["product_id", "product_name", "thumbnail_url", "quantity", "unit_price_cents"];

    for (let j = 0; j < order.items.length; j++) {
      const item = order.items[j];

      for (const field of itemFields) {
        if (item[field] !== undefined && item[field] !== null) {
          pass(`items[${j}].${field} present`);
        } else {
          fail(`items[${j}].${field} missing`);
        }
      }

      // thumbnail_url looks like a URL
      if (item.thumbnail_url && item.thumbnail_url.startsWith("http")) {
        pass(`items[${j}].thumbnail_url is a valid URL`);
      } else {
        fail(`items[${j}].thumbnail_url does not look like a URL`, `Got: ${item.thumbnail_url}`);
      }

      // quantity is positive integer
      if (Number.isInteger(item.quantity) && item.quantity >= 1) {
        pass(`items[${j}].quantity = ${item.quantity} (valid)`);
      } else {
        fail(`items[${j}].quantity invalid`, `Expected positive integer, got: ${item.quantity}`);
      }

      // unit_price_cents is integer
      if (Number.isInteger(item.unit_price_cents)) {
        pass(`items[${j}].unit_price_cents is integer (${item.unit_price_cents})`);
      } else {
        fail(`items[${j}].unit_price_cents is not an integer`);
      }
    }
  }

  // -------------------------------------------------------
  // HC-F2: No N+1 pattern needed
  // -------------------------------------------------------
  console.log("\n[HC-F2] No N+1 pattern — product data is inline");

  let allItemsHaveProductData = true;
  for (const order of data.orders) {
    for (const item of order.items || []) {
      if (!item.product_name || !item.thumbnail_url) {
        allItemsHaveProductData = false;
      }
    }
  }

  if (allItemsHaveProductData) {
    pass("All items have product_name and thumbnail_url inline — no follow-up requests needed");
  } else {
    fail("Some items missing product_name or thumbnail_url — would require N+1 fetches");
  }

  // -------------------------------------------------------
  // Summary
  // -------------------------------------------------------
  console.log("\n=== RESULT ===");
  console.log(`  ${passCount} passed, ${failCount} failed`);

  if (failCount === 0) {
    console.log("  OVERALL: PASS — All HC-F constraints satisfied.");
    process.exit(0);
  } else {
    console.log("  OVERALL: FAIL — Some constraints not met.");
    process.exit(1);
  }
}

main();
