#!/usr/bin/env python3
"""
Client validator for GET /dashboard/orders.
Fetches from the mock server and validates the response structure
against the agreed API spec (final_api_spec.yaml).

Usage: python3 client_validator.py [--url URL]
Default URL: http://localhost:8080/dashboard/orders?page=1&page_size=20
"""

import json
import sys
import urllib.request
import urllib.error
from datetime import datetime

MOCK_SERVER_URL = "http://localhost:8080/dashboard/orders?page=1&page_size=20"

VALID_STATUSES = {"pending", "confirmed", "shipped", "delivered", "cancelled", "returned"}

REQUIRED_ORDER_FIELDS = {
    "order_id": str,
    "status": str,
    "total_cents": int,
    "currency": str,
    "created_at": str,
    "total_items_count": int,
    "items": list,
}

REQUIRED_ITEM_FIELDS = {
    "product_id": str,
    "product_name": str,
    "product_image_url": str,
    "unit_price_cents": int,
    "quantity": int,
}

REQUIRED_PAGINATION_FIELDS = {
    "page": int,
    "page_size": int,
    "total_orders": int,
    "total_pages": int,
}


def fail(msg):
    print(f"FAIL: {msg}")
    return False


def validate_iso8601(value, context):
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except (ValueError, AttributeError):
        return fail(f"{context}: '{value}' is not a valid ISO 8601 datetime")


def validate_uri(value, context):
    if not (value.startswith("http://") or value.startswith("https://")):
        return fail(f"{context}: '{value}' is not a valid URI (must start with http:// or https://)")
    return True


def validate_fields(obj, required_fields, context):
    ok = True
    for field, expected_type in required_fields.items():
        if field not in obj:
            fail(f"{context}: missing required field '{field}'")
            ok = False
            continue
        if not isinstance(obj[field], expected_type):
            fail(f"{context}.{field}: expected {expected_type.__name__}, got {type(obj[field]).__name__}")
            ok = False
    return ok


def validate_item(item, context):
    ok = validate_fields(item, REQUIRED_ITEM_FIELDS, context)
    if not ok:
        return False

    if not validate_uri(item["product_image_url"], f"{context}.product_image_url"):
        ok = False

    if item["quantity"] < 1:
        fail(f"{context}.quantity: must be >= 1, got {item['quantity']}")
        ok = False

    return ok


def validate_order(order, index):
    context = f"orders[{index}]"
    ok = validate_fields(order, REQUIRED_ORDER_FIELDS, context)
    if not ok:
        return False

    # Validate status enum
    if order["status"] not in VALID_STATUSES:
        fail(f"{context}.status: '{order['status']}' not in valid statuses {VALID_STATUSES}")
        ok = False

    # Validate created_at is ISO 8601
    if not validate_iso8601(order["created_at"], f"{context}.created_at"):
        ok = False

    # Validate total_items_count >= 1
    if order["total_items_count"] < 1:
        fail(f"{context}.total_items_count: must be >= 1, got {order['total_items_count']}")
        ok = False

    # Validate items array max 3
    if len(order["items"]) > 3:
        fail(f"{context}.items: max 3 items allowed, got {len(order['items'])}")
        ok = False

    # Validate items count consistency
    if order["total_items_count"] < len(order["items"]):
        fail(f"{context}: total_items_count ({order['total_items_count']}) < items length ({len(order['items'])})")
        ok = False

    # Validate each item
    for i, item in enumerate(order["items"]):
        if not validate_item(item, f"{context}.items[{i}]"):
            ok = False

    return ok


def validate_pagination(pagination):
    context = "pagination"
    ok = validate_fields(pagination, REQUIRED_PAGINATION_FIELDS, context)
    if not ok:
        return False

    if pagination["page"] < 1:
        fail(f"{context}.page: must be >= 1, got {pagination['page']}")
        ok = False

    if pagination["page_size"] < 1 or pagination["page_size"] > 50:
        fail(f"{context}.page_size: must be 1-50, got {pagination['page_size']}")
        ok = False

    if pagination["total_orders"] < 0:
        fail(f"{context}.total_orders: must be >= 0, got {pagination['total_orders']}")
        ok = False

    if pagination["total_pages"] < 0:
        fail(f"{context}.total_pages: must be >= 0, got {pagination['total_pages']}")
        ok = False

    return ok


def validate_response(data):
    ok = True

    # Top-level required fields
    if "orders" not in data:
        return fail("Response missing required field 'orders'")
    if "pagination" not in data:
        return fail("Response missing required field 'pagination'")

    if not isinstance(data["orders"], list):
        return fail(f"'orders' must be an array, got {type(data['orders']).__name__}")
    if not isinstance(data["pagination"], dict):
        return fail(f"'pagination' must be an object, got {type(data['pagination']).__name__}")

    # Validate each order
    for i, order in enumerate(data["orders"]):
        if not isinstance(order, dict):
            fail(f"orders[{i}]: expected object, got {type(order).__name__}")
            ok = False
            continue
        if not validate_order(order, i):
            ok = False

    # Validate pagination
    if not validate_pagination(data["pagination"]):
        ok = False

    return ok


def main():
    url = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else None
    if url is None:
        for i, arg in enumerate(sys.argv[1:], 1):
            if arg == "--url" and i < len(sys.argv) - 1:
                url = sys.argv[i + 1]
                break
    if url is None:
        url = MOCK_SERVER_URL

    print(f"Fetching: {url}")

    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                print(f"FAIL: Expected HTTP 200, got {resp.status}")
                sys.exit(1)

            content_type = resp.headers.get("Content-Type", "")
            if "application/json" not in content_type:
                print(f"FAIL: Expected Content-Type application/json, got '{content_type}'")
                sys.exit(1)

            body = resp.read().decode("utf-8")

    except urllib.error.URLError as e:
        print(f"FAIL: Could not connect to {url}: {e}")
        sys.exit(1)

    try:
        data = json.loads(body)
    except json.JSONDecodeError as e:
        print(f"FAIL: Response is not valid JSON: {e}")
        sys.exit(1)

    print(f"Response received: {len(data.get('orders', []))} orders")
    print("---")

    if validate_response(data):
        print("---")
        print("PASS: All validations passed.")
        print(f"  Orders: {len(data['orders'])}")
        print(f"  Page: {data['pagination']['page']}/{data['pagination']['total_pages']}")
        sys.exit(0)
    else:
        print("---")
        print("FAIL: Validation errors found (see above).")
        sys.exit(1)


if __name__ == "__main__":
    main()
