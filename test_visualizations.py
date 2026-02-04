#!/usr/bin/env python3
"""Test embedding visualizations"""

from app import app
import json

client = app.test_client()

print("Testing embedding visualizations...\n")

# Test TF-IDF visualization
print("1. Testing TF-IDF with visualization")
response = client.post("/demo/tfidf", json={
    "documents": ["cat dog bird", "dog cat fox", "bird fox owl"]
})

if response.status_code == 200:
    data = response.get_json()
    if data.get('status') == 'success':
        if data.get('visualization'):
            print("   ✓ TF-IDF visualization generated!")
            viz = data['visualization']
            print(f"     - Type: {viz.get('data', [{}])[0].get('type', 'unknown')}")
            print(f"     - Title: {viz.get('layout', {}).get('title', 'N/A')}")
            print(f"     - Points: {len(viz.get('data', [{}])[0].get('x', []))}")
            print(f"   ✓ Metadata: {json.dumps(data.get('viz_metadata', {}), indent=6)}")
        else:
            print("   ✗ No visualization generated")
    else:
        print(f"   ✗ Error: {data.get('message')}")
else:
    print(f"   ✗ Status: {response.status_code}")

# Test SGNS visualization
print("\n2. Testing SGNS with visualization")
response = client.post("/demo/sgns", json={
    "corpus": ["the cat sat", "the dog ran", "the bird flew"]
})

if response.status_code == 200:
    data = response.get_json()
    if data.get('status') == 'success':
        if data.get('visualization'):
            print("   ✓ SGNS visualization generated!")
            viz = data['visualization']
            print(f"     - Type: {viz.get('data', [{}])[0].get('type', 'unknown')}")
            print(f"     - Title: {viz.get('layout', {}).get('title', 'N/A')}")
            print(f"     - Points (words): {len(viz.get('data', [{}])[0].get('x', []))}")
            print(f"   ✓ Metadata: {json.dumps(data.get('viz_metadata', {}), indent=6)}")
        else:
            print("   ✗ No visualization generated")
    else:
        print(f"   ✗ Error: {data.get('message')}")
else:
    print(f"   ✗ Status: {response.status_code}")

print("\n✅ Visualization tests complete!")
