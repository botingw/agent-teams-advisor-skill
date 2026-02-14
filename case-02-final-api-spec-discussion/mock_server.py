"""
Mock server for GET /dashboard/orders.
Generates realistic fake data matching final_api_spec.yaml.
Python stdlib only — no external dependencies.

Usage:
    python mock_server.py
    # Server starts on http://localhost:8080
    # Try: curl "http://localhost:8080/dashboard/orders?page=1&page_size=5"
"""

import json
import math
import random
import string
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta, timezone

# Seed for reproducible data
random.seed(42)

# --- Fake data pools ---

PRODUCT_NAMES = [
    "Wireless Headphones", "USB-C Cable", "Mechanical Keyboard",
    "Laptop Stand", "Webcam HD", "Mouse Pad XL", "Monitor Light Bar",
    "Portable SSD 1TB", "Bluetooth Speaker", "Phone Case",
    "Screen Protector", "Charging Dock", "Smart Watch Band",
    "Desk Organizer", "Cable Management Kit", "Ergonomic Mouse",
    "Noise Cancelling Earbuds", "Tablet Stylus", "Power Bank 20000mAh",
    "HDMI Adapter",
]

STATUSES = ["pending", "confirmed", "shipped", "delivered", "cancelled", "returned"]

TOTAL_ORDERS = 127  # Simulated total for a single user


def _generate_product_id(index):
    return f"prod_{index:04d}"


def _generate_order_id(index):
    return f"ord_{index:05d}"


def _generate_image_url(product_id):
    return f"https://cdn.example.com/products/{product_id}/thumb.webp"


def _generate_order(order_index):
    """Generate a single order with deterministic but realistic data."""
    rng = random.Random(order_index)
    total_items_count = rng.randint(1, 8)
    preview_count = min(total_items_count, 3)

    items = []
    order_total = 0
    for i in range(preview_count):
        prod_index = rng.randint(0, len(PRODUCT_NAMES) - 1)
        product_id = _generate_product_id(prod_index)
        unit_price = rng.randint(299, 9999)
        quantity = rng.randint(1, 4)
        order_total += unit_price * quantity
        items.append({
            "product_id": product_id,
            "product_name": PRODUCT_NAMES[prod_index],
            "product_image_url": _generate_image_url(product_id),
            "unit_price_cents": unit_price,
            "quantity": quantity,
        })

    # Add cost for non-preview items to total
    for i in range(total_items_count - preview_count):
        order_total += rng.randint(299, 9999) * rng.randint(1, 4)

    days_ago = TOTAL_ORDERS - order_index
    created = datetime(2025, 1, 1, tzinfo=timezone.utc) + timedelta(
        days=days_ago, hours=rng.randint(0, 23), minutes=rng.randint(0, 59)
    )

    return {
        "order_id": _generate_order_id(order_index),
        "status": rng.choice(STATUSES),
        "total_cents": order_total,
        "currency": "USD",
        "created_at": created.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_items_count": total_items_count,
        "items": items,
    }


# Pre-generate all orders (sorted newest first)
ALL_ORDERS = [_generate_order(i) for i in range(TOTAL_ORDERS)]
ALL_ORDERS.sort(key=lambda o: o["created_at"], reverse=True)


class DashboardHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path != "/dashboard/orders":
            self._send_json(404, {"error": "Not found"})
            return

        params = parse_qs(parsed.query)
        try:
            page = int(params.get("page", ["1"])[0])
            page_size = int(params.get("page_size", ["20"])[0])
        except ValueError:
            self._send_json(400, {"error": "page and page_size must be integers"})
            return

        if page < 1:
            self._send_json(400, {"error": "page must be >= 1"})
            return
        if page_size < 1 or page_size > 50:
            self._send_json(400, {"error": "page_size must be between 1 and 50"})
            return

        total_orders = len(ALL_ORDERS)
        total_pages = max(1, math.ceil(total_orders / page_size))
        start = (page - 1) * page_size
        end = start + page_size
        orders_page = ALL_ORDERS[start:end]

        response = {
            "orders": orders_page,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_orders": total_orders,
                "total_pages": total_pages,
            },
        }
        self._send_json(200, response)

    def _send_json(self, status_code, data):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")


def main():
    host = "localhost"
    port = 8080
    server = HTTPServer((host, port), DashboardHandler)
    print(f"Mock server running on http://{host}:{port}")
    print(f"Try: curl http://{host}:{port}/dashboard/orders?page=1&page_size=5")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
