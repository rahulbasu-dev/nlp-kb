#!/usr/bin/env python3
"""Final comprehensive endpoint test"""

from app import app

client = app.test_client()

print("=" * 60)
print("FINAL COMPREHENSIVE ENDPOINT TEST")
print("=" * 60)
print()

tests = [
    ("GET /", client.get, "/", None),
    ("GET /docs", client.get, "/docs", None),
    ("GET /lessons", client.get, "/lessons", None),
    ("GET /lessons/quick", client.get, "/lessons/quick", None),
    ("GET /lessons/standard", client.get, "/lessons/standard", None),
    ("GET /lessons/comprehensive", client.get, "/lessons/comprehensive", None),
    ("POST /demo/tfidf", client.post, "/demo/tfidf", {"documents": ["hello world", "world peace"]}),
    ("POST /demo/sgns", client.post, "/demo/sgns", {"corpus": ["the cat sat", "the dog ran"]}),
    ("GET /examples", client.get, "/examples", None),
    ("GET /examples/1", client.get, "/examples/1", None),
]

passed = 0
failed = 0

for name, method, path, data in tests:
    try:
        if data is None:
            response = method(path)
        else:
            response = method(path, json=data)
        
        if response.status_code in [200, 302]:  # 302 for redirects
            status_indicator = "✓"
            passed += 1
        else:
            status_indicator = "✗"
            failed += 1
        
        print(f"{status_indicator} {name:30s} → {response.status_code}")
    except Exception as e:
        print(f"✗ {name:30s} → ERROR: {str(e)[:40]}")
        failed += 1

print()
print("=" * 60)
print(f"Results: {passed} passed, {failed} failed")
print("=" * 60)
