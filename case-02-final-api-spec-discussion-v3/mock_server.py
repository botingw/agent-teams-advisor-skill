"""Mock server for GET /dashboard/orders matching final_api_spec.yaml."""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

MOCK_ORDERS = [
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
                "unit_price_cents": 2500,
            },
            {
                "product_id": "prod_002",
                "product_name": "Phone Case",
                "thumbnail_url": "https://cdn.example.com/thumbs/prod_002_64x64.jpg",
                "quantity": 2,
                "unit_price_cents": 1000,
            },
        ],
    },
    {
        "id": "order_def456",
        "status": "shipped",
        "total_cents": 8999,
        "currency": "USD",
        "created_at": "2025-01-10T14:22:00Z",
        "items": [
            {
                "product_id": "prod_003",
                "product_name": "USB-C Hub",
                "thumbnail_url": "https://cdn.example.com/thumbs/prod_003_64x64.jpg",
                "quantity": 1,
                "unit_price_cents": 8999,
            },
        ],
    },
    {
        "id": "order_ghi789",
        "status": "pending",
        "total_cents": 1299,
        "currency": "USD",
        "created_at": "2025-01-08T09:15:00Z",
        "items": [
            {
                "product_id": "prod_004",
                "product_name": "Screen Protector",
                "thumbnail_url": "https://cdn.example.com/thumbs/prod_004_64x64.jpg",
                "quantity": 1,
                "unit_price_cents": 1299,
            },
        ],
    },
    {
        "id": "order_jkl012",
        "status": "confirmed",
        "total_cents": 15498,
        "currency": "USD",
        "created_at": "2025-01-05T16:45:00Z",
        "items": [
            {
                "product_id": "prod_005",
                "product_name": "Mechanical Keyboard",
                "thumbnail_url": "https://cdn.example.com/thumbs/prod_005_64x64.jpg",
                "quantity": 1,
                "unit_price_cents": 12999,
            },
            {
                "product_id": "prod_006",
                "product_name": "Wrist Rest",
                "thumbnail_url": "https://cdn.example.com/thumbs/prod_006_64x64.jpg",
                "quantity": 1,
                "unit_price_cents": 2499,
            },
        ],
    },
    {
        "id": "order_mno345",
        "status": "cancelled",
        "total_cents": 3200,
        "currency": "USD",
        "created_at": "2025-01-02T11:00:00Z",
        "items": [
            {
                "product_id": "prod_007",
                "product_name": "Laptop Stand",
                "thumbnail_url": "https://cdn.example.com/thumbs/prod_007_64x64.jpg",
                "quantity": 1,
                "unit_price_cents": 3200,
            },
        ],
    },
]

TOTAL_ORDERS = len(MOCK_ORDERS)


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != "/dashboard/orders":
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
            return

        params = parse_qs(parsed.query)
        try:
            limit = int(params.get("limit", ["10"])[0])
            offset = int(params.get("offset", ["0"])[0])
        except ValueError:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": "limit and offset must be integers"}).encode()
            )
            return

        limit = max(1, min(limit, 50))
        offset = max(0, offset)

        paginated = MOCK_ORDERS[offset : offset + limit]

        response = {
            "orders": paginated,
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total": TOTAL_ORDERS,
            },
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        print(f"[mock_server] {args[0]}")


def main():
    port = 8080
    server = HTTPServer(("localhost", port), DashboardHandler)
    print(f"Mock server running on http://localhost:{port}")
    print(f"Try: http://localhost:{port}/dashboard/orders")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
