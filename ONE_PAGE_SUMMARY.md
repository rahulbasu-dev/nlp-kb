# One-Page SGNS Summary for Students

## Skip-gram with Negative Sampling (SGNS) at a Glance

```
┌─────────────────────────────────────────────────────────────────────┐
│                     THE BIG PICTURE                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  INPUT: Text corpus ("the cat sat on the mat")                       │
│         ↓                                                             │
│  LEARN: Word embeddings (vectors representing word meanings)        │
│         ↓                                                             │
│  OUTPUT: 50-300 dimensional vectors where similar words are close  │
│                                                                       │
│  WHY: Words in similar contexts → similar meanings                  │
│       "king" and "queen" → similar vectors                          │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Algorithm Overview

```
STEP 1: INITIALIZE
  • Random word embeddings (D-dimensional vectors)
  • For each word in vocabulary

STEP 2: TRAINING LOOP
  For each word in corpus:
    a) GET CONTEXT WINDOW
       └─ Words within distance 'window_size' of target
    
    b) POSITIVE SAMPLING
       └─ Use actual context words
    
    c) NEGATIVE SAMPLING  
       └─ Sample k random words from vocabulary
    
    d) UPDATE EMBEDDINGS
       • Maximize: dot(target, context_word)
       • Minimize: dot(target, random_word)
       • Use gradient descent to move vectors

STEP 3: REPEAT
  • Multiple epochs until convergence
```

## Example: One Training Step

```
Sentence: "the cat sat on the mat"
Target word: "cat" (position 1)
Window size: 2
Negative samples: 1

┌─────────────────────────────────────┐
│ Context words (actual):             │
│ • "the" (position 0)                │
│ • "sat" (position 2)                │
│ Action: MAXIMIZE similarity         │
│ ✓ Pull vectors closer               │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Negative samples (random):          │
│ • "dog" (random word)               │
│ Action: MINIMIZE similarity         │
│ ✓ Push vectors apart                │
└─────────────────────────────────────┘
```

## Why "Negative" Sampling?

```
PROBLEM: Computing softmax over 1M vocabulary words is SLOW
         Cost = O(vocabulary_size) per training step

SOLUTION: Use negative sampling
         • Keep 1 positive sample (real context)
         • Add k negative samples (random words)
         • Cost = O(k) where k = 5-20

BENEFIT: 100,000x FASTER! ⚡
```

## Key Concepts

| Concept | Meaning |
|---------|---------|
| **Embedding** | Vector representation of a word |
| **Context Window** | Nearby words (typically ±2 words) |
| **Positive Sample** | Real context word (we want high similarity) |
| **Negative Sample** | Random word (we want low similarity) |
| **Dot Product** | Measure of vector similarity |
| **Sigmoid** | Function that outputs 0-1 probability |
| **Gradient** | Direction to update weights |
| **Epoch** | One full pass through entire corpus |

## The Learning Mechanism

```
TARGET: "king"  ────────────────────────────────────────
                │
                ├─ POSITIVE: "queen"   → similarity ↑ (0.3 → 0.8)
                │                       vector moves closer
                │
                └─ NEGATIVES:           
                   • "dog"              → similarity ↓ (0.5 → 0.1)
                   • "table"            → similarity ↓ (0.4 → 0.0)
                   vectors move apart

RESULT: After many iterations, "king" and "queen" have similar vectors
```

## Hyperparameters (What You Can Tune)

```
embedding_dim = 100          (Higher = richer but slower)
learning_rate = 0.025        (Higher = faster but unstable)
window_size = 2              (Larger = more context)
negative_samples = 5         (More = smoother learning)
epochs = 10                  (More = better convergence)
```

## Applications

```
✓ Finding similar words
✓ Word analogies (king - man + woman ≈ queen)
✓ Clustering documents
✓ Feature extraction for ML models
✓ Recommendation systems
✓ Semantic search
```

## Important Formulas

```
1. DOT PRODUCT (similarity measure):
   sim = v_word1 · v_word2 = Σ(v_word1[i] * v_word2[i])

2. SIGMOID (convert to probability):
   σ(x) = 1 / (1 + e^-x)  →  outputs [0, 1]

3. LOSS FOR POSITIVE SAMPLE:
   loss = -log(σ(dot_product))

4. LOSS FOR NEGATIVE SAMPLE:
   loss = -log(1 - σ(dot_product)) = -log(σ(-dot_product))

5. GRADIENT UPDATE:
   v_new = v_old + learning_rate × gradient
```

## Learning Progression

```
EPOCH 1:    Embeddings still mostly random
            ├─ "king" and "queen" somewhat similar
            └─ "dog" and "cat" somewhat similar

EPOCH 5:    Patterns emerging
            ├─ "king" and "queen" very similar
            ├─ "dog" and "cat" very similar
            └─ Gender words cluster together

EPOCH 10:   Convergence
            ├─ Related words in same region
            ├─ Unrelated words far apart
            └─ Stable embeddings for downstream tasks

EPOCH 20+:  Marginal improvements
            ├─ Fine-tuning rather than learning
            └─ Returns diminish
```

## Quick Implementation Checklist

```
□ Initialize random embeddings
□ Build vocabulary from corpus
□ For each epoch:
  □ For each word in corpus:
    □ Get context window
    □ For each context word:
      □ Compute dot product with target
      □ Compute sigmoid(dot_product)
      □ Compute positive sample loss
      □ Update embeddings
    □ For k negative samples:
      □ Compute dot product with target
      □ Compute sigmoid(dot_product)
      □ Compute negative sample loss
      □ Update embeddings
□ Save embeddings for downstream use
```

## Common Questions

**Q: Why use sigmoid instead of softmax?**
A: Sigmoid gives independent probability for each sample. Softmax sums to 1, not needed here.

**Q: Why sample negatives from freq^0.75?**
A: Empirical finding - balances between uniform and frequency-weighted sampling.

**Q: Can I use embeddings for any task?**
A: Generally yes! They capture word meanings learned from corpus context.

**Q: How many dimensions do I need?**
A: 50-100 for small corpora, 100-300 for large. More dimensions = more expressive but slower.

**Q: Is SGNS still used?**
A: Less common now (replaced by contextual embeddings like BERT), but foundational to understanding modern NLP.

---

**Master these concepts → You understand word embeddings! 🎓**
