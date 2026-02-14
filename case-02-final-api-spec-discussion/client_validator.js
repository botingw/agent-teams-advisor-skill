/**
 * Client Validator for GET /dashboard/orders
 * Project Legacy Phoenix — Frontend validation
 *
 * Fetches from the mock server and validates the response matches
 * the agreed API spec (final_api_spec.yaml). Ensures all fields
 * needed for order card rendering are present and correctly typed.
 *
 * Usage: node client_validator.js [base_url]
 *   base_url defaults to http://localhost:8080
 */

const BASE_URL = process.argv[2] || "http://localhost:8080";
const ENDPOINT = "/dashboard/orders";

const VALID_STATUSES = ["pending", "processing", "shipped", "delivered", "cancelled"];
const VALID_SORTS = ["created_at:desc", "created_at:asc", "total_amount:desc", "total_amount:asc"];

let passCount = 0;
let failCount = 0;

function check(label, condition, detail) {
  if (condition) {
    passCount++;
    console.log(`  PASS: ${label}`);
  } else {
    failCount++;
    console.log(`  FAIL: ${label}${detail ? ` — ${detail}` : ""}`);
  }
}

function isNonEmptyString(val) {
  return typeof val === "string" && val.length > 0;
}

function isPositiveNumber(val) {
  return typeof val === "number" && val > 0;
}

function isNonNegativeInteger(val) {
  return Number.isInteger(val) && val >= 0;
}

function isPositiveInteger(val) {
  return Number.isInteger(val) && val > 0;
}

function isISO8601(val) {
  if (typeof val !== "string") return false;
  const d = new Date(val);
  return !isNaN(d.getTime());
}

function isURL(val) {
  if (typeof val !== "string") return false;
  try {
    new URL(val);
    return true;
  } catch {
    return false;
  }
}

function validateOrderItem(item, index, orderIndex) {
  const prefix = `orders[${orderIndex}].items[${index}]`;
  check(`${prefix}.product_id is a non-empty string`, isNonEmptyString(item.product_id), `got ${JSON.stringify(item.product_id)}`);
  check(`${prefix}.product_name is a non-empty string`, isNonEmptyString(item.product_name), `got ${JSON.stringify(item.product_name)}`);
  check(`${prefix}.thumbnail_url is a valid URL`, isURL(item.thumbnail_url), `got ${JSON.stringify(item.thumbnail_url)}`);
  check(`${prefix}.quantity is a positive integer`, isPositiveInteger(item.quantity), `got ${JSON.stringify(item.quantity)}`);
  check(`${prefix}.unit_price is a positive number`, isPositiveNumber(item.unit_price), `got ${JSON.stringify(item.unit_price)}`);
}

function validateOrder(order, index) {
  const prefix = `orders[${index}]`;

  // Required fields existence
  check(`${prefix}.order_id is a non-empty string`, isNonEmptyString(order.order_id), `got ${JSON.stringify(order.order_id)}`);
  check(`${prefix}.status is a valid enum`, VALID_STATUSES.includes(order.status), `got ${JSON.stringify(order.status)}`);
  check(`${prefix}.created_at is ISO 8601`, isISO8601(order.created_at), `got ${JSON.stringify(order.created_at)}`);
  check(`${prefix}.total_amount is a positive number`, isPositiveNumber(order.total_amount), `got ${JSON.stringify(order.total_amount)}`);
  check(`${prefix}.currency is a non-empty string`, isNonEmptyString(order.currency), `got ${JSON.stringify(order.currency)}`);
  check(`${prefix}.item_count is a non-negative integer`, isNonNegativeInteger(order.item_count), `got ${JSON.stringify(order.item_count)}`);

  // Items array
  check(`${prefix}.items is an array`, Array.isArray(order.items), `got ${typeof order.items}`);
  if (Array.isArray(order.items)) {
    check(`${prefix}.items is non-empty`, order.items.length > 0, "items array is empty");
    check(`${prefix}.item_count matches items.length`, order.item_count === order.items.length, `item_count=${order.item_count} but items.length=${order.items.length}`);

    // Validate items sorted by unit_price DESC
    if (order.items.length > 1) {
      const sorted = order.items.every((item, i) => {
        if (i === 0) return true;
        return item.unit_price <= order.items[i - 1].unit_price;
      });
      check(`${prefix}.items sorted by unit_price DESC`, sorted, "items are not sorted by unit_price descending");
    }

    // Validate each item
    order.items.forEach((item, i) => validateOrderItem(item, i, index));
  }

  // Card rendering check: first item must have thumbnail + name for card display
  if (Array.isArray(order.items) && order.items.length > 0) {
    const firstItem = order.items[0];
    check(`${prefix} card render: first item has thumbnail_url`, isURL(firstItem.thumbnail_url), "missing thumbnail for card");
    check(`${prefix} card render: first item has product_name`, isNonEmptyString(firstItem.product_name), "missing product name for card");
  }
}

function validatePagination(pagination) {
  check("pagination is an object", typeof pagination === "object" && pagination !== null, `got ${typeof pagination}`);
  if (typeof pagination !== "object" || pagination === null) return;

  check("pagination.page is a positive integer", isPositiveInteger(pagination.page), `got ${JSON.stringify(pagination.page)}`);
  check("pagination.page_size is a positive integer", isPositiveInteger(pagination.page_size), `got ${JSON.stringify(pagination.page_size)}`);
  check("pagination.page_size <= 50", typeof pagination.page_size === "number" && pagination.page_size <= 50, `got ${pagination.page_size}`);
  check("pagination.total_count is a non-negative integer", isNonNegativeInteger(pagination.total_count), `got ${JSON.stringify(pagination.total_count)}`);
  check("pagination.total_pages is a non-negative integer", isNonNegativeInteger(pagination.total_pages), `got ${JSON.stringify(pagination.total_pages)}`);
}

async function fetchOrders(params = {}) {
  const url = new URL(`${BASE_URL}${ENDPOINT}`);
  for (const [key, value] of Object.entries(params)) {
    url.searchParams.set(key, value);
  }
  const response = await fetch(url.toString());
  return { status: response.status, data: await response.json() };
}

async function runValidation() {
  console.log(`\nClient Validator — GET ${ENDPOINT}`);
  console.log(`Target: ${BASE_URL}`);
  console.log("=".repeat(60));

  // Test 1: Default request
  console.log("\n[Test 1] Default request (no params)");
  const { status, data } = await fetchOrders();
  check("HTTP status is 200", status === 200, `got ${status}`);
  check("Response has 'orders' array", Array.isArray(data.orders), `got ${typeof data.orders}`);
  check("Response has 'pagination' object", typeof data.pagination === "object", `got ${typeof data.pagination}`);

  if (Array.isArray(data.orders)) {
    check("orders array is non-empty", data.orders.length > 0, "no orders returned");
    check("orders count <= default page_size (20)", data.orders.length <= 20, `got ${data.orders.length}`);

    console.log(`\n  Validating ${data.orders.length} orders...`);
    data.orders.forEach((order, i) => validateOrder(order, i));
  }

  if (data.pagination) {
    console.log("\n  Validating pagination...");
    validatePagination(data.pagination);
  }

  // Test 2: With query params
  console.log("\n[Test 2] Request with params (page=1, page_size=5, sort=total_amount:desc)");
  const { status: s2, data: d2 } = await fetchOrders({ page: 1, page_size: 5, sort: "total_amount:desc" });
  check("HTTP status is 200", s2 === 200, `got ${s2}`);
  if (Array.isArray(d2.orders)) {
    check("orders count <= requested page_size (5)", d2.orders.length <= 5, `got ${d2.orders.length}`);
  }
  if (d2.pagination) {
    check("pagination.page_size reflects request", d2.pagination.page_size === 5, `got ${d2.pagination.page_size}`);
  }

  // Test 3: Status filter
  console.log("\n[Test 3] Request with status filter (status=shipped)");
  const { status: s3, data: d3 } = await fetchOrders({ status: "shipped" });
  check("HTTP status is 200", s3 === 200, `got ${s3}`);
  if (Array.isArray(d3.orders)) {
    const allShipped = d3.orders.every((o) => o.status === "shipped");
    check("All returned orders have status 'shipped'", allShipped, "found orders with non-shipped status");
  }

  // Summary
  console.log("\n" + "=".repeat(60));
  console.log(`RESULTS: ${passCount} passed, ${failCount} failed`);
  if (failCount === 0) {
    console.log("All validations PASSED — response matches spec for card rendering.");
  } else {
    console.log("Some validations FAILED — response does not fully match spec.");
  }
  console.log();

  process.exit(failCount > 0 ? 1 : 0);
}

runValidation().catch((err) => {
  console.error(`\nFATAL: Could not connect to ${BASE_URL}${ENDPOINT}`);
  console.error(`Error: ${err.message}`);
  console.error("Is the mock server running?");
  process.exit(2);
});
