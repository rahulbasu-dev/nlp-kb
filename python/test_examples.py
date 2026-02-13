#!/usr/bin/env python
"""Direct test of classroom examples without menu input."""

import sys
sys.path.insert(0, '.')

from classroom_examples import (
    example_1_basic_usage,
    example_8_tfidf_basics,
    example_9_sgns_vs_tfidf
)

print("\n" + "="*70)
print("Running Example 8: TF-IDF Basics")
print("="*70)
example_8_tfidf_basics()

print("\n\n" + "="*70)
print("Running Example 9: SGNS vs TF-IDF Comparison")
print("="*70)
example_9_sgns_vs_tfidf()
