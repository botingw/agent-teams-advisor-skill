# EXECUTIVE DIRECTIVE: Project Legacy Phoenix
# PRIORITY: P0 (CRITICAL BLOCKER)

## Context
We are launching the "Mobile Order Dashboard" next week. The requirements are finalized, but we have a critical architectural deadlock between Backend and Frontend teams.

## The Objective
Finalize the API contract for the `GET /dashboard/orders` endpoint immediately. We need a `final_api_spec.yaml` (OpenAPI 3.0) that satisfies all constraints.

## Team Roles & Constraints

### 1. @Backend_Lead (Python/SQL Expert)
**Priority:** System Stability & DB Health.
- **Constraint:** The `orders` table has 50M rows. The `products` table is sharded separately.
- **Hard Rule:** You CANNOT perform joins across shards in the database. You strictly prefer fetching IDs only or doing a very simple fan-out.
- **Goal:** Protect the DB CPU usage. Reject any schema proposal that requires complex joins on high-volume queries.

### 2. @Frontend_Lead (React/Performance Expert)
**Priority:** Core Web Vitals (LCP < 2.5s).
- **Constraint:** Target audience uses 4G networks. We have a strict budget of **1 HTTP request** to render the "Above the Fold" content.
- **Hard Rule:** You cannot accept a design that requires fetching a list of orders and then firing N+1 requests for product images.
- **Goal:** Get a single JSON response that has everything needed to render the cards immediately.

## Workflow
1.  **Architectural Debate:** Debate the JSON structure and architectural pattern (e.g., BFF, Data Loading strategy, Aggregation Layer).
2.  **Contract Agreement:** Create `final_api_spec.yaml`.
3.  **Implementation:**
    - Backend: Create a mock server generating data matching the spec.
    - Frontend: Create a client script to fetch and validate the data structure against UI needs.