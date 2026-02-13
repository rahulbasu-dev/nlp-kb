#!/usr/bin/env python3
"""Comprehensive functionality test for NLP Classroom after cleanup."""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_route(url, description):
    """Test a single route."""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✓ {description}")
            return True
        else:
            print(f"✗ {description} (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"✗ {description} (Error: {str(e)})")
        return False

def test_api(url, description):
    """Test an API endpoint."""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ {description} - Returns: {type(data).__name__}")
            return True
        else:
            print(f"✗ {description} (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"✗ {description} (Error: {str(e)})")
        return False

def test_demo(url, description, payload):
    """Test a demo endpoint with POST."""
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"✓ {description} - Demo works!")
                return True
            else:
                print(f"✗ {description} - Error: {data.get('message', 'Unknown')}")
                return False
        else:
            print(f"✗ {description} (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"✗ {description} (Error: {str(e)})")
        return False

def main():
    """Run all tests."""
    print("=" * 70)
    print("NLP CLASSROOM - COMPREHENSIVE FUNCTIONALITY TEST")
    print("=" * 70)
    print()
    
    passed = 0
    failed = 0
    
    # Wait for server to be ready
    print("Waiting for Flask server...")
    time.sleep(2)
    
    print("\n--- TESTING MAIN ROUTES ---")
    tests = [
        (f"{BASE_URL}/", "Homepage"),
        (f"{BASE_URL}/lessons/tfidf", "TF-IDF Lesson Page"),
        (f"{BASE_URL}/lessons/sgns", "SGNS Lesson Page"),
        (f"{BASE_URL}/lessons/comparison", "Comparison Lesson Page"),
    ]
    
    for url, desc in tests:
        if test_route(url, desc):
            passed += 1
        else:
            failed += 1
    
    print("\n--- TESTING DEMO PAGES ---")
    tests = [
        (f"{BASE_URL}/demo/tfidf", "TF-IDF Demo Page"),
        (f"{BASE_URL}/demo/sgns", "SGNS Demo Page"),
    ]
    
    for url, desc in tests:
        if test_route(url, desc):
            passed += 1
        else:
            failed += 1
    
    print("\n--- TESTING CLASSROOM MODE ---")
    tests = [
        (f"{BASE_URL}/classroom", "Classroom Landing Page"),
        (f"{BASE_URL}/classroom/lesson/quick", "Quick Lesson (15 min)"),
        (f"{BASE_URL}/classroom/lesson/standard", "Standard Lesson (30 min)"),
        (f"{BASE_URL}/classroom/lesson/comprehensive", "Comprehensive Lesson (60 min)"),
    ]
    
    for url, desc in tests:
        if test_route(url, desc):
            passed += 1
        else:
            failed += 1
    
    print("\n--- TESTING RESOURCES ---")
    tests = [
        (f"{BASE_URL}/visualizations", "Visualizations Gallery"),
        (f"{BASE_URL}/examples", "Code Examples List"),
        (f"{BASE_URL}/docs", "Documentation Hub"),
    ]
    
    for url, desc in tests:
        if test_route(url, desc):
            passed += 1
        else:
            failed += 1
    
    print("\n--- TESTING API ENDPOINTS ---")
    if test_api(f"{BASE_URL}/api/available-visualizations", "Available Visualizations API"):
        passed += 1
    else:
        failed += 1
    
    print("\n--- TESTING INTERACTIVE DEMOS ---")
    
    # Test TF-IDF demo
    tfidf_payload = {
        'documents': [
            'machine learning is amazing',
            'natural language processing rocks',
            'machine learning and nlp together'
        ]
    }
    if test_demo(f"{BASE_URL}/demo/tfidf", "TF-IDF Demo Computation", tfidf_payload):
        passed += 1
    else:
        failed += 1
    
    # Test SGNS demo
    sgns_payload = {
        'corpus': [
            'the cat sat on the mat',
            'the dog sat on the log',
            'cats and dogs are friends'
        ],
        'params': {
            'embedding_dim': 30,
            'window_size': 2,
            'negative_samples': 5,
            'epochs': 5
        }
    }
    if test_demo(f"{BASE_URL}/demo/sgns", "SGNS Demo Training", sgns_payload):
        passed += 1
    else:
        failed += 1
    
    # Summary
    print("\n" + "=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)
    
    if failed == 0:
        print("\n✓ ALL TESTS PASSED! No functionality lost during cleanup.")
        return 0
    else:
        print(f"\n✗ {failed} tests failed. Some functionality may be missing.")
        return 1

if __name__ == '__main__':
    exit(main())
