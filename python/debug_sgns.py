#!/usr/bin/env python3
"""Debug /demo/sgns endpoint"""

from app import app
import json

client = app.test_client()

print("Debugging /demo/sgns endpoint...\n")

response = client.post("/demo/sgns", json={
    "corpus": [["the", "cat", "sat"], ["the", "dog", "ran"]]
})

print(f"Status Code: {response.status_code}")
print(f"Full Response:")
print(json.dumps(response.get_json(), indent=2))
