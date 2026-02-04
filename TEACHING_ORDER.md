# Teaching Order: TF-IDF First, Then SGNS

## Rationale

The teaching materials are now organized to introduce **TF-IDF first**, then **Skip-gram with Negative Sampling (SGNS)** second. This pedagogical order is optimal because:

1. **TF-IDF is simpler and more interpretable** - Students understand formulas and statistics more easily than neural network concepts
2. **TF-IDF provides a foundation** - Before learning contextual embeddings, students should understand statistical importance
3. **SGNS builds naturally** - After learning TF-IDF, SGNS concepts make more sense as a more sophisticated alternative
4. **Natural complexity progression** - Moves from simple (statistics) to complex (deep learning)

---

## Recommended Teaching Sequence

### Phase 1: TF-IDF (Statistical Approach)
**Duration:** 15-20 minutes

**Visualizations to show:**
1. `01_tfidf_matrix.png` - Show how words get importance scores
2. `02_idf_distribution.png` - Explain why rare words matter more
3. `03_tfidf_similarities.png` - Show document comparisons

**Interactive demo:**
```bash
python sgns.py
# Select option 2: TF-IDF Only Demo
```

**Key concepts:**
- Term Frequency (TF): How often a word appears
- Inverse Document Frequency (IDF): Rarity bonus for distinctive words
- TF-IDF = TF × IDF: Combines frequency with importance
- Very fast, fully interpretable method
- Perfect for document search and classification

---

### Phase 2: Method Comparison (Bridge)
**Duration:** 5-10 minutes

**Visualizations to show:**
4. `04_sgns_vs_tfidf_comparison.png` - Side-by-side comparison

**Key concepts:**
- TF-IDF: Statistical, interpretable, fast
- SGNS: Semantic, contextual, requires training
- When to use each method
- Trade-offs between speed and sophistication

---

### Phase 3: SGNS (Semantic Embeddings)
**Duration:** 20-30 minutes

**Visualizations to show (in order):**
5. `05_context_window.png` - Explain the core mechanism
6. `06_sampling_process.png` - Show why negative sampling is efficient
7. `07_embeddings_2d.png` - Prove it learns meaningful relationships
8. `08_similarity_heatmap.png` - Quantify learned similarities
9. `09_algorithm_steps.png` - Walk through step-by-step
10. `10_training_dynamics.png` - Show convergence over time
11. `11_infographic_sgns.png` - Summary overview

**Interactive demo:**
```bash
python sgns.py
# Select option 1: SGNS Only Demo
```

**Key concepts:**
- Skip-gram: Predict context from target word
- Negative Sampling: Efficient alternative to softmax
- Context Window: Learn from nearby words
- Dense embeddings: Capture semantic relationships
- Requires training but captures analogies

---

### Phase 4: Integration & Exploration
**Duration:** 10-15 minutes

**Interactive demos:**
```bash
# Option 1: See SGNS alone
python sgns.py → 1

# Option 2: See TF-IDF alone  
python sgns.py → 2

# Option 3: See both side-by-side
python sgns.py → 3

# Option 4: See complete tour
python sgns.py → 4
```

**Interactive examples:**
```bash
python classroom_examples.py
# Try examples:
#   1. Basic Usage (SGNS)
#   2. Hyperparameter Impact
#   3. Context Window Effect
#   8. TF-IDF Basics
#   9. SGNS vs TF-IDF Comparison
```

---

## Complete Teaching Timeline

### 30-Minute Quickstart
```
5 min  - TF-IDF overview: Show visualizations 01-03
5 min  - TF-IDF demo: Run python sgns.py (option 2)
5 min  - Show comparison: Visualization 04
10 min - SGNS overview: Show visualizations 05-06, 11
5 min  - Wrap-up and Q&A
```

### 60-Minute Comprehensive Lesson
```
10 min - TF-IDF fundamentals (explain formula)
5 min  - TF-IDF visualizations 01-03
5 min  - Interactive TF-IDF demo (sgns.py option 2)
5 min  - Comparison visualization 04
15 min - SGNS fundamentals (explain algorithm)
10 min - SGNS visualizations 05-09
5 min  - Interactive SGNS demo (sgns.py option 1)
5 min  - Conclusion: When to use each method
```

### 90-Minute Deep Dive
```
15 min - TF-IDF theory, practice, & limitations
10 min - All TF-IDF visualizations with discussion
5 min  - TF-IDF interactive demo
5 min  - Comparison overview
20 min - SGNS theory and mathematics
15 min - All SGNS visualizations with deep explanations
10 min - SGNS interactive demo + parameter tuning
5 min  - Live comparison: sgns.py option 3
5 min  - Student questions and exploration
```

---

## File Organization Reference

### Python Code Files
- **`sgns.py`** - Core algorithms + TFIDF class + interactive menu (1, 2, 3, or 4 options)
- **`classroom_examples.py`** - 9 interactive demonstrations (examples 1-9)
- **`sgns_visualization.py`** - Generates all 11 PNG files

### Markdown Documentation
- **`START_HERE.md`** - Entry point for all users
- **`README.md`** - Complete overview with menu instructions
- **`INDEX.md`** - Quick navigation and decision tree
- **`TEACHING_CHEATSHEET.md`** - Instructor reference card (with TF-IDF section)
- **`VISUALIZATION_GUIDE.md`** - How to use each of the 11 graphics
- **`ONE_PAGE_SUMMARY.md`** - Student cheat sheet
- **`00_READ_ME_FIRST.md`** - Master orientation document
- **`TEACHING_ORDER.md`** - This file: pedagogical sequencing

### Visualization Files (11 PNG files)

**TF-IDF First (4 files):**
```
01_tfidf_matrix.png           ← Document-term importance matrix
02_idf_distribution.png       ← Word rarity/importance distribution
03_tfidf_similarities.png     ← Document similarity heatmap
04_sgns_vs_tfidf_comparison.png ← Method comparison table
```

**SGNS Second (7 files):**
```
05_context_window.png         ← Core concept: sliding window
06_sampling_process.png       ← Core innovation: negative sampling
07_embeddings_2d.png          ← Learned word relationships (t-SNE)
08_similarity_heatmap.png     ← Quantified word similarities
09_algorithm_steps.png        ← Step-by-step algorithm flow
10_training_dynamics.png      ← How embeddings improve with training
11_infographic_sgns.png       ← Complete summary overview
```

---

## Quick Reference: When to Use Each

### Use TF-IDF When:
✓ Speed is critical (no training needed)
✓ You need interpretable word importance
✓ Working with document search/classification
✓ You have small to medium corpora
✓ You need to explain decisions to non-technical stakeholders

### Use SGNS When:
✓ You need semantic/contextual understanding
✓ You want word analogies (king - man + woman = queen)
✓ You're building NLP systems (translation, Q&A, etc.)
✓ You have large amounts of unlabeled text
✓ You want to capture meaning relationships

### Use Both When:
✓ Teaching both methods for comparison
✓ You want to establish a baseline (TF-IDF) before trying SGNS
✓ You're doing research or benchmarking
✓ You want students to understand the evolution of NLP techniques
