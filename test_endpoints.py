#!/usr/bin/env python3
"""Test the problem endpoints after SGNS fix"""

import requests
import json

BASE_URL = "http://localhost:5000"

print("Testing the three problem endpoints...\n")

# Test 1: /demo/tfidf
print("1. Testing POST /demo/tfidf")
try:
    response = requests.post(f"{BASE_URL}/demo/tfidf", json={
        "documents": ["machine learning is great", "deep learning is powerful"]
    })
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            print("   ✓ /demo/tfidf works!")
        else:
            print(f"   ✗ /demo/tfidf returned error: {result.get('error')}")
    else:
        print(f"   ✗ /demo/tfidf failed with status {response.status_code}")
except Exception as e:
    print(f"   ✗ /demo/tfidf error: {e}")

# Test 2: /demo/sgns
print("\n2. Testing POST /demo/sgns")
try:
    response = requests.post(f"{BASE_URL}/demo/sgns", json={
        "corpus": [["the", "cat", "sat"], ["the", "dog", "ran"]]
    })
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            print("   ✓ /demo/sgns works!")
        else:
            print(f"   ✗ /demo/sgns returned error: {result.get('error')}")
    else:
        print(f"   ✗ /demo/sgns failed with status {response.status_code}")
except Exception as e:
    print(f"   ✗ /demo/sgns error: {e}")

# Test 3: /examples/1
print("\n3. Testing GET /examples/1")
try:
    response = requests.get(f"{BASE_URL}/examples/1")
    if response.status_code == 200:
        print("   ✓ /examples/1 loads!")
    else:
        print(f"   ✗ /examples/1 failed with status {response.status_code}")
except Exception as e:
    print(f"   ✗ /examples/1 error: {e}")

print("\n✅ Testing complete!")
