#!/usr/bin/env python
"""
Test script for SGNS Training Dynamics Visualization
Verifies all components work correctly
"""

import requests
import json
import time

BASE_URL = 'http://localhost:5000'

def test_endpoint_exists():
    """Test that the endpoint is accessible."""
    print("\n" + "="*70)
    print("TEST 1: Endpoint Accessibility")
    print("="*70)
    
    try:
        response = requests.get(f'{BASE_URL}/demo/sgns-training-dynamics')
        if response.status_code == 200:
            print("✅ PASS: Endpoint is accessible")
            print(f"   Status code: {response.status_code}")
            return True
        else:
            print(f"❌ FAIL: Unexpected status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ FAIL: Could not reach endpoint: {str(e)}")
        return False


def test_animation_visualization():
    """Test animation visualization generation."""
    print("\n" + "="*70)
    print("TEST 2: Animation Visualization Generation")
    print("="*70)
    
    corpus = [
        "the cat sat on the mat",
        "the dog sat on the floor",
        "the bird flew in the sky"
    ]
    
    params = {
        'embedding_dim': 20,
        'window_size': 2,
        'negative_samples': 5,
        'epochs': 5,
        'capture_interval': 1,
        'learning_rate': 0.025,
        'method': 'pca'
    }
    
    try:
        print(f"Sending request with {len(corpus)} sentences...")
        print(f"Training for {params['epochs']} epochs...")
        
        start_time = time.time()
        response = requests.post(
            f'{BASE_URL}/demo/sgns-training-dynamics',
            json={
                'corpus': corpus,
                'params': params,
                'viz_type': 'animation'
            },
            timeout=30
        )
        elapsed = time.time() - start_time
        
        if response.status_code != 200:
            print(f"❌ FAIL: Status code {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
        
        data = response.json()
        
        # Verify response structure
        required_keys = ['status', 'visualization', 'viz_type', 'metadata']
        for key in required_keys:
            if key not in data:
                print(f"❌ FAIL: Missing key in response: {key}")
                return False
        
        # Verify visualization structure
        viz = data['visualization']
        viz_keys = ['data', 'frames', 'layout']
        for key in viz_keys:
            if key not in viz:
                print(f"❌ FAIL: Missing key in visualization: {key}")
                return False
        
        # Verify metadata
        metadata = data['metadata']
        print(f"\n✅ PASS: Animation visualization generated")
        print(f"   Vocab size: {metadata['vocab_size']}")
        print(f"   Epochs: {metadata['epochs']}")
        print(f"   Embedding dim: {metadata['embedding_dim']}")
        print(f"   Method: {metadata['method']}")
        print(f"   Frames: {len(viz['frames'])}")
        print(f"   Time: {elapsed:.2f}s")
        
        return True
        
    except requests.Timeout:
        print("❌ FAIL: Request timed out")
        return False
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_distance_visualization():
    """Test distance progression visualization."""
    print("\n" + "="*70)
    print("TEST 3: Distance Progression Visualization")
    print("="*70)
    
    corpus = [
        "cat dog bird",
        "dog bird cat",
        "bird cat dog"
    ]
    
    params = {
        'embedding_dim': 15,
        'window_size': 1,
        'negative_samples': 3,
        'epochs': 5,
        'capture_interval': 1,
        'method': 'pca'
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/demo/sgns-training-dynamics',
            json={
                'corpus': corpus,
                'params': params,
                'viz_type': 'distance'
            },
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ FAIL: Status code {response.status_code}")
            return False
        
        data = response.json()
        viz = data['visualization']
        
        # Verify distance visualization has traces (line chart)
        if 'data' not in viz or len(viz['data']) == 0:
            print("❌ FAIL: No data traces in visualization")
            return False
        
        print("✅ PASS: Distance visualization generated")
        print(f"   Number of traces: {len(viz['data'])}")
        for i, trace in enumerate(viz['data']):
            if 'name' in trace:
                print(f"   Trace {i+1}: {trace['name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        return False


def test_heatmap_visualization():
    """Test similarity heatmap evolution."""
    print("\n" + "="*70)
    print("TEST 4: Similarity Heatmap Visualization")
    print("="*70)
    
    corpus = [
        "apple orange banana",
        "orange banana apple",
        "banana apple orange"
    ]
    
    params = {
        'embedding_dim': 15,
        'window_size': 1,
        'negative_samples': 3,
        'epochs': 3,
        'capture_interval': 1,
        'method': 'pca'
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/demo/sgns-training-dynamics',
            json={
                'corpus': corpus,
                'params': params,
                'viz_type': 'heatmap'
            },
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ FAIL: Status code {response.status_code}")
            return False
        
        data = response.json()
        viz = data['visualization']
        
        # Verify heatmap structure
        if 'frames' not in viz or len(viz['frames']) == 0:
            print("❌ FAIL: No frames in heatmap visualization")
            return False
        
        print("✅ PASS: Heatmap visualization generated")
        print(f"   Number of frames: {len(viz['frames'])}")
        print(f"   Frame names: {[f['name'] for f in viz['frames']]}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAIL: {str(e)}")
        return False


def test_edge_cases():
    """Test edge cases and error handling."""
    print("\n" + "="*70)
    print("TEST 5: Edge Cases & Error Handling")
    print("="*70)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Empty corpus
    tests_total += 1
    try:
        response = requests.post(
            f'{BASE_URL}/demo/sgns-training-dynamics',
            json={
                'corpus': [],
                'params': {'epochs': 5},
                'viz_type': 'animation'
            },
            timeout=10
        )
        if response.status_code != 200:
            print("✅ PASS: Empty corpus rejected")
            tests_passed += 1
        else:
            print("❌ FAIL: Empty corpus should be rejected")
    except:
        print("✅ PASS: Empty corpus error handled")
        tests_passed += 1
    
    # Test 2: Single sentence corpus
    tests_total += 1
    try:
        response = requests.post(
            f'{BASE_URL}/demo/sgns-training-dynamics',
            json={
                'corpus': ["one two three"],
                'params': {
                    'embedding_dim': 10,
                    'window_size': 1,
                    'negative_samples': 2,
                    'epochs': 2,
                    'capture_interval': 1,
                    'method': 'pca'
                },
                'viz_type': 'animation'
            },
            timeout=10
        )
        if response.status_code == 200:
            print("✅ PASS: Single sentence handled")
            tests_passed += 1
        else:
            print("❌ FAIL: Single sentence failed")
    except Exception as e:
        print(f"❌ FAIL: Single sentence error: {str(e)}")
    
    # Test 3: Very small embedding
    tests_total += 1
    try:
        response = requests.post(
            f'{BASE_URL}/demo/sgns-training-dynamics',
            json={
                'corpus': ["a b c d"],
                'params': {
                    'embedding_dim': 2,
                    'window_size': 1,
                    'negative_samples': 1,
                    'epochs': 1,
                    'capture_interval': 1,
                    'method': 'pca'
                },
                'viz_type': 'animation'
            },
            timeout=10
        )
        if response.status_code == 200:
            print("✅ PASS: Minimal embedding handled")
            tests_passed += 1
        else:
            print("❌ FAIL: Minimal embedding failed")
    except Exception as e:
        print(f"❌ FAIL: Minimal embedding error: {str(e)}")
    
    print(f"\nEdge case tests: {tests_passed}/{tests_total} passed")
    return tests_passed == tests_total


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("SGNS TRAINING DYNAMICS - TEST SUITE")
    print("="*70)
    
    tests = [
        ("Endpoint Accessibility", test_endpoint_exists),
        ("Animation Visualization", test_animation_visualization),
        ("Distance Visualization", test_distance_visualization),
        ("Heatmap Visualization", test_heatmap_visualization),
        ("Edge Cases", test_edge_cases),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ EXCEPTION in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*70)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("="*70)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("Training Dynamics feature is fully functional!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("Please check the errors above")
    
    return passed == total


if __name__ == '__main__':
    main()
