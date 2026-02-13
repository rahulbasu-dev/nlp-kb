#!/usr/bin/env python3
"""Test SGNS model fix for small vocabularies"""

from sgns import SkipGramNegativeSampling

# Test with small corpus (same as demo)
corpus = [['the', 'cat', 'sat'], ['the', 'dog', 'ran']]

print('Testing SGNS with small corpus...')
try:
    model = SkipGramNegativeSampling(embedding_dim=10, negative_samples=5)
    model.build_vocab(corpus)
    model.train(corpus, epochs=2)
    print('✓ SGNS training successful on small corpus!')
    print(f'  Vocabulary size: {len(model.vocab)}')
    print(f'  Embedding dim: {model.embedding_dim}')
except Exception as e:
    print(f'✗ SGNS training failed: {e}')
    import traceback
    traceback.print_exc()
