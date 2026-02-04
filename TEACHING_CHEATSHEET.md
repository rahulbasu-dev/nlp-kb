# SGNS Teaching Cheat Sheet

## What is Skip-gram with Negative Sampling?

**One-liner**: A fast algorithm to learn word meanings by predicting context words and using negative sampling to reduce training cost.

---

## The Core Idea (30 seconds)

```
Words that appear in similar contexts → should have similar meanings
                                     ↓
Skip-gram learns this by:
  • Looking at words near a target word (context window)
  • Predicting context words from the target word
  • Using negative sampling to make it fast
```

---

## Algorithm at a Glance

```
FOR each word in text:
  ├─ Get context words within window (positive samples)
  ├─ Sample random words (negative samples)  
  ├─ Maximize: similarity(target, context_word)
  └─ Minimize: similarity(target, random_word)
```

---

## Why "Negative Sampling"?

| Method | Cost | Speed |
|--------|------|-------|
| Softmax over 1M vocab | O(V) = 1M ops | ❌ Slow |
| Negative Sampling (k=5) | O(k) = 5 ops | ✅ 200x faster |

---

## Quick Demo Script

```python
# Import and train
from sgns import SkipGramNegativeSampling

sentences = [
    ["king", "is", "a", "man"],
    ["queen", "is", "a", "woman"],
]

model = SkipGramNegativeSampling()
model.build_vocab(sentences)
model.train(sentences, epochs=10)

# Find similar words
similar = model.most_similar("king", topn=3)
print(similar)  # [(queen, 0.89), ...]
```

---

## Key Hyperparameters

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| `embedding_dim` | 100 | 50-300 | Higher = more expressive |
| `learning_rate` | 0.025 | 0.001-0.1 | Lower = more stable |
| `window_size` | 2 | 1-10 | Larger = more context |
| `negative_samples` | 5 | 2-20 | More = more stable |
| `epochs` | varies | 5-20 | More = better convergence |

---

## What Students Should Understand

✓ **Conceptually**
- Words with similar contexts have similar meanings
- Neural networks can learn embeddings through gradient descent
- Negative sampling is a clever way to make training fast

✓ **Technically**
- How context window slides over text
- Positive vs negative sampling strategy
- Gradient updates (push similar words closer, dissimilar words apart)
- Why embeddings can be used for downstream tasks

✓ **Practically**
- How to train a model on corpus
- How to find similar words (cosine similarity)
- How parameters affect learning
- Why this matters (foundation for modern NLP)

---

## Common Questions

**Q: Why 0.75 power for negative sampling probabilities?**
A: Empirical finding - slightly favors common words for negatives, prevents rare words from dominating.

**Q: Why two embedding matrices (target + context)?**
A: Pragmatic choice - could share weights but separate matrices work well in practice.

**Q: Can I use these embeddings for downstream tasks?**
A: Yes! Use the target word vectors. They're pre-trained representations for: classification, clustering, similarity tasks, etc.

**Q: How is this different from modern approaches?**
A: SGNS is foundational (2013), but Transformers (2017+) learn better contextual embeddings (words have different meanings in different contexts).

---

## Visualization Map

| Need | Visualization | 
|------|----------------|
| Explain sliding window | `01_context_window.png` |
| Show why negative sampling is clever | `02_sampling_process.png` |
| Prove it learns meanings | `03_embeddings_2d.png` + `04_similarity_heatmap.png` |
| Walk through algorithm | `05_algorithm_steps.png` |
| Show learning over time | `06_training_dynamics.png` |
| Quick overview/summary | `07_infographic.png` |

---

## Classroom Flow

```
5 min: Show infographic (what is SGNS?)
10 min: Show context window + sampling (how does it work?)
10 min: Demo running sgns.py (live interaction)
10 min: Analyze embeddings visualization (what did it learn?)
5 min: Show similarity heatmap (quantify results)
10 min: Discuss hyperparameters and variations
5 min: Wrap-up and modern connections
```

**Total: ~55 minutes**

---

## TF-IDF: A Complementary Approach

**What is TF-IDF?**
- **TF** (Term Frequency): How often a word appears in a document
- **IDF** (Inverse Document Frequency): How unique the word is across all documents
- **TF-IDF** = TF × IDF: Weight showing how important a word is to a specific document

**Formula:**
```
TF(word, doc) = count(word in doc) / total_words_in_doc
IDF(word) = log(total_documents / documents_containing_word)
TF-IDF = TF × IDF
```

**How SGNS and TF-IDF Compare:**

| Aspect | SGNS | TF-IDF |
|--------|------|--------|
| **What it learns** | Word meanings (semantic) | Word importance (statistical) |
| **Input** | Raw text corpus | Document-term matrix |
| **Output** | Dense vectors (50-300D) | Sparse vectors (vocab-size D) |
| **Speed** | Slower (gradient descent) | Fast (formula-based) |
| **Use case** | Finding similar words, embeddings | Document search, feature extraction |
| **Context** | Uses word proximity | Ignores word order |
| **Modern? ** | Foundational (2013) | Classic (1980s-2000s) |

**When to Use Each:**
- **Use SGNS** when you need:
  - Semantic word relationships ("king"/"queen" similarity)
  - Transfer learning (embeddings for other tasks)
  - Finding synonyms and analogies
  
- **Use TF-IDF** when you need:
  - Fast document similarity
  - Document search/retrieval
  - Interpretable feature importance
  - No deep learning infrastructure

**Key Difference:**
```
SGNS: "Words mean what they predict" (contextual)
TF-IDF: "Words matter if they're rare in corpus" (statistical)
```

**Example:**
```
Sentence: "The cat sat on the mat"
Word "cat":
  • SGNS: Vector [0.5, 0.2, ...] (learned similarity to "dog", "sat")
  • TF-IDF: High weight (rare/unique), low if in every document
```

---

## Talking Points

1. **Context is key**: "Words are defined by the company they keep" - this is the core insight

2. **Efficiency matters**: "Training on 1B word corpus would take forever with softmax. Negative sampling makes it practical."

3. **It's contrastive learning**: "We're not just learning to predict - we're learning to distinguish signal from noise"

4. **Foundation for modern NLP**: "SGNS inspired Word2vec, which influenced how we think about embeddings in transformers"

5. **Applications everywhere**: "Any NLP task that needs word relationships can benefit from these embeddings"

---

## Hands-On Exercise Ideas

1. **Change hyperparameters** - show how embedding_dim and learning_rate affect results
2. **Visualize different corpora** - see how embeddings change with different text
3. **Test analogies** - "king - man + woman ≈ queen" (math on embeddings)
4. **Downstream tasks** - use embeddings for document classification
5. **Compare with random embeddings** - show why learning matters

---

**Pro Tip**: Run visualizations before class. Generate them once, then show during teaching!
