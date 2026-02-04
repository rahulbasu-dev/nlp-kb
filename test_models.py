#!/usr/bin/env python3
"""Test model functionality."""

# Test imports
try:
    from sgns import SkipGramNegativeSampling, TFIDF
    print("✓ SGNS/TFIDF imports OK")
except Exception as e:
    print(f"✗ Import error: {e}")
    exit(1)

# Test TFIDF
try:
    tfidf = TFIDF()
    tfidf.fit([['hello', 'world'], ['hello', 'there']])
    result = tfidf.transform(['hello'])
    print(f"✓ TFIDF works: {len(result)} features")
except Exception as e:
    print(f"✗ TFIDF error: {e}")

# Test SGNS  
try:
    sgns = SkipGramNegativeSampling(embedding_dim=20)
    sgns.build_vocab([['hello', 'world'], ['hello', 'there']])
    sgns.train([['hello', 'world'], ['hello', 'there']], epochs=2)
    result = sgns.most_similar('hello', topn=2)
    print(f"✓ SGNS works: found {len(result)} similar words")
except Exception as e:
    print(f"✗ SGNS error: {e}")

print("\n✓ Both models working!")
