#!/usr/bin/env python3
"""Test /demo/sgns with correct format"""

from app import app

client = app.test_client()

print("Testing /demo/sgns with string corpus format...\n")

response = client.post("/demo/sgns", json={
    "corpus": ["the cat sat", "the dog ran"]
})

if response.status_code == 200:
    result = response.get_json()
    if result.get('status') == 'success':
        print("✓ /demo/sgns works!")
        print(f"  Model trained with vocab size: {result.get('vocab_size')}")
    else:
        print(f"✗ Error: {result.get('message')}")
else:
    print(f"✗ Status: {response.status_code}")
