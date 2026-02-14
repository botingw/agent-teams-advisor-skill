# Mobile Order Dashboard — API Contract & Mock Implementation

## Overview

This project finalizes the API contract for the `GET /dashboard/orders` endpoint of the Mobile Order Dashboard. It was produced by an Agent Teams sprint (Project Legacy Phoenix) with a Backend Lead and Frontend Lead negotiating the contract under conflicting constraints.

## Architecture

**Pattern:** Cache-Assisted Fan-Out (BFF)

The orders table has 50M rows and the products table is on a separate shard. Cross-shard joins are impossible at the DB level. The solution:

1. Query the `orders` table with simple pagination (limit/offset) — no joins
2. Collect unique product IDs from the result set
3. Batch-fetch product data (name, thumbnail URL) via `IN(product_id1, product_id2, ...)` from the product shard
4. Embed product data inline in each order item at the application layer
5. Return a single JSON response with everything needed to render order cards

This satisfies both sides:
- **Backend:** No cross-shard joins. Simple fan-out with batch lookup. Sustainable DB CPU usage.
- **Frontend:** Single HTTP request. All data inline (no N+1). Payload under 50KB for 4G networks.

## Files

| File | Description |
|------|-------------|
| `final_api_spec.yaml` | OpenAPI 3.0 specification for `GET /dashboard/orders` |
| `mock_server.py` | Python mock server (stdlib only) serving sample data matching the spec |
| `client_validator.js` | Node.js client that fetches from the mock server and validates response structure |
| `MISSION_CONTEXT.md` | Constitution File — team roles, constraints, communication protocol |
| `PROJECT_RETROSPECTIVE.md` | Post-sprint retrospective with categorized insights |
| `update_skill_proposal.md` | Proposed improvements to the agent-teams-advisor skill |
| `mission.md` | Original mission directive |

## How to Run

### Prerequisites
- Python 3.8+
- Node.js 18+ (uses native `fetch`)

### Start the Mock Server

```bash
python case-02-final-api-spec-discussion/mock_server.py
```

The server starts on `http://localhost:8080`. Test manually:

```bash
curl http://localhost:8080/dashboard/orders
curl "http://localhost:8080/dashboard/orders?limit=2&offset=1"
```

### Run the Client Validator

In a separate terminal (while the mock server is running):

```bash
node case-02-final-api-spec-discussion/client_validator.js
```

Expected output: `115 passed, 0 failed — OVERALL: PASS`

### End-to-End Test (Single Command)

```bash
python case-02-final-api-spec-discussion/mock_server.py &
sleep 1
node case-02-final-api-spec-discussion/client_validator.js
kill %1
```

## API Endpoint

### `GET /dashboard/orders`

**Query Parameters:**

| Param | Type | Default | Range | Description |
|-------|------|---------|-------|-------------|
| `limit` | integer | 10 | 1–50 | Orders per page |
| `offset` | integer | 0 | 0+ | Orders to skip |

**Response (200):**

```json
{
  "orders": [
    {
      "id": "order_abc123",
      "status": "delivered",
      "total_cents": 4500,
      "currency": "USD",
      "created_at": "2025-01-15T10:30:00Z",
      "items": [
        {
          "product_id": "prod_001",
          "product_name": "Wireless Earbuds",
          "thumbnail_url": "https://cdn.example.com/thumbs/prod_001_64x64.jpg",
          "quantity": 1,
          "unit_price_cents": 2500
        }
      ]
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "total": 42
  }
}
```

**Status enum values:** `pending`, `confirmed`, `shipped`, `delivered`, `cancelled`

## Key Architectural Decisions

| Decision | Rationale |
|----------|-----------|
| Cache-Assisted Fan-Out over denormalized read model | Avoids write amplification on product updates. Batch `IN(...)` lookup is cheap and satisfies single-request constraint. |
| limit/offset over cursor-based pagination | Order history is append-mostly, sorted by `created_at DESC`. Offset drift is minimal for dashboard use case. |
| Integer cents for money (`total_cents`, `unit_price_cents`) | Avoids floating-point precision issues in financial data. Standard industry practice. |
| Pre-resized 64x64 thumbnails via CDN URL | Reduces payload size. Frontend renders thumbnails directly without resizing. |
| Product data inline in order items | Eliminates N+1 requests. Frontend gets everything in 1 HTTP call for above-the-fold rendering. |
