# Project Legacy Phoenix — Mobile Order Dashboard API

## Overview

This project finalizes the API contract for `GET /dashboard/orders`, an endpoint for the Mobile Order Dashboard. The API was designed through a structured debate between Backend and Frontend leads, resolving the architectural tension between database scalability (50M row orders table with sharded products) and frontend performance (LCP < 2.5s on 4G with a single HTTP request).

## Architecture

**Pattern: Backend-for-Frontend (BFF) Aggregation Layer**

```
┌──────────┐     1 HTTP      ┌─────────┐    fan-out     ┌────────────┐
│ Frontend  │ ──────────────→ │   BFF   │ ─────────────→ │ Orders DB  │
│ (React)   │ ←────────────── │  Layer  │ ←───────────── │ (50M rows) │
└──────────┘   single JSON   │         │                └────────────┘
                              │         │    batch-fetch  ┌────────────┐
                              │         │ ─────────────→ │ Products   │
                              │         │ ←───────────── │ (sharded)  │
                              └─────────┘                └────────────┘
```

The BFF layer:
1. Queries the orders DB with a simple indexed query (`user_id` + `created_at DESC`) — no cross-shard joins
2. Batch-fetches product details (name, image URL, price) from the sharded products service
3. Assembles and returns a single pre-aggregated JSON response

### Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Pagination | Offset-based (`page` + `page_size`) | Per-user order counts are manageable (hundreds to low thousands); offset is simple and efficient with composite index |
| Items per order | Capped at 3 preview items + `total_items_count` | Keeps payload small for 4G; frontend shows "+N more" link |
| Prices | Integer cents (`total_cents`, `unit_price_cents`) | Avoids floating-point precision issues in JSON |
| Status | Enum: pending, confirmed, shipped, delivered, cancelled, returned | Standard e-commerce lifecycle |
| Images | CDN URLs in response (`product_image_url`) | Eliminates N+1 image fetch requests |

## Files

| File | Description |
|------|-------------|
| `final_api_spec.yaml` | OpenAPI 3.0.3 specification for `GET /dashboard/orders` |
| `mock_server.py` | Python mock server generating realistic data matching the spec |
| `client_validator.py` | Python client that fetches and validates the response structure |
| `MISSION_CONTEXT.md` | Constitution file used to coordinate the Backend/Frontend team |
| `PROJECT_RETROSPECTIVE.md` | Post-mortem analysis of the team collaboration session |
| `mission.md` | Original mission directive |

## Running the Code

### Prerequisites
- Python 3.7+
- No external dependencies (stdlib only)

### Start the Mock Server

```bash
cd case-02-final-api-spec-discussion
python mock_server.py
# Server starts on http://localhost:8080
```

### Test with curl

```bash
curl "http://localhost:8080/dashboard/orders?page=1&page_size=5"
```

### Run the Client Validator

In a separate terminal (while the mock server is running):

```bash
python client_validator.py
# Or with a custom URL:
python client_validator.py --url "http://localhost:8080/dashboard/orders?page=2&page_size=10"
```

Expected output:
```
Fetching: http://localhost:8080/dashboard/orders?page=1&page_size=20
Response received: 20 orders
---
---
PASS: All validations passed.
  Orders: 20
  Page: 1/7
```

## API Quick Reference

```
GET /dashboard/orders?page=1&page_size=20

Response:
{
  "orders": [
    {
      "order_id": "ord_00126",
      "status": "shipped",
      "total_cents": 4999,
      "currency": "USD",
      "created_at": "2025-01-15T10:30:00Z",
      "total_items_count": 5,
      "items": [              // max 3 preview items
        {
          "product_id": "prod_0012",
          "product_name": "Wireless Headphones",
          "product_image_url": "https://cdn.example.com/products/prod_0012/thumb.webp",
          "unit_price_cents": 2499,
          "quantity": 2
        }
      ]
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_orders": 127,
    "total_pages": 7
  }
}
```
