# Skip-gram with Negative Sampling & TF-IDF - Classroom Visualizations

This directory contains comprehensive visualizations designed to explain Skip-gram with Negative Sampling (SGNS) and TF-IDF in a classroom setting.

## Files Overview (in recommended teaching order)

### 📊 TF-IDF Visualizations (Teach First - Simpler & More Interpretable)

1. **`01_tfidf_matrix.png`** - Document-Term Matrix
   - Heatmap showing TF-IDF scores for each word in each document
   - Red = high importance, Yellow = medium, White = low
   - Shows which words are important for document identification
   - **Use case**: Explain how TF-IDF weights word importance statistically
   - **Complexity**: Low - just a formula, very interpretable

2. **`02_idf_distribution.png`** - Word Importance Distribution
   - Bar chart of IDF (Inverse Document Frequency) values
   - Green bars: Rare words (high IDF, high importance)
   - Orange bars: Medium frequency words
   - Red bars: Common words (low IDF, low importance)
   - **Use case**: Show why TF-IDF downweights common words and emphasizes distinctive ones
   - **Complexity**: Low - direct visual of word rarity

3. **`03_tfidf_similarities.png`** - Document Similarity
   - Heatmap showing cosine similarity between documents using TF-IDF
   - Documents about similar topics have higher similarity scores
   - Perfect comparison with SGNS word similarity
   - **Use case**: Demonstrate that TF-IDF captures document relationships
   - **Complexity**: Medium - simple cosine distance calculation

4. **`04_sgns_vs_tfidf_comparison.png`** - Method Comparison
   - Side-by-side comparison table
   - What each method learns (semantic vs statistical)
   - Key characteristics (speed, training, interpretability)
   - When to use each method
   - **Use case**: Help students decide which method to use for their problem
   - **Complexity**: Medium - introduces SGNS concepts for comparison

### 📊 Skip-gram Visualizations (Teach After TF-IDF - More Complex)

5. **`05_context_window.png`** - Context Window Mechanism
   - Shows how a sliding window moves over a sentence
   - Red: Target word
   - Green: Context words (within the window)
   - Gray: Words outside the window
   - **Use case**: Explain how SGNS learns by looking at nearby words
   - **Complexity**: Medium - introduces the context concept

6. **`06_sampling_process.png`** - Positive vs Negative Sampling
   - Left panel: Positive sampling (maximize similarity with context words)
   - Right panel: Negative sampling (minimize similarity with random words)
   - **Use case**: Core concept of why SGNS is efficient (1 positive + k negatives, not full vocabulary)
   - **Complexity**: High - key innovation requiring explanation

7. **`07_embeddings_2d.png`** - Word Embeddings Space
   - Shows word vectors projected to 2D using t-SNE
   - Color-coded by word category (Gender words, Functions, Objects)
   - Similar words cluster together
   - **Use case**: Demonstrate that the model learns meaningful relationships
   - **Complexity**: High - requires understanding embeddings and t-SNE

8. **`08_similarity_heatmap.png`** - Similarity Matrix
   - Heatmap showing cosine similarity between word pairs
   - Green = high similarity, Red = low similarity
   - Shows that "king"/"queen" and "man"/"woman" are similar
   - **Use case**: Quantify the learned relationships
   - **Complexity**: High - requires understanding learned embeddings

9. **`09_algorithm_steps.png`** - Algorithm Flow
   - 5-step breakdown of the SGNS algorithm
   - Step 1: Input corpus
   - Step 2: Slide context window
   - Step 3: Positive sampling
   - Step 4: Negative sampling
   - Step 5: Update embeddings
   - **Use case**: Walk through the algorithm step-by-step
   - **Complexity**: High - requires understanding all components

10. **`10_training_dynamics.png`** - How Embeddings Evolve
    - Shows embeddings after 1, 5, 10, and 20 epochs of training
    - Demonstrates convergence toward meaningful representations
    - **Use case**: Show that training improves word relationships over time
    - **Complexity**: High - shows learning dynamics

11. **`11_infographic_sgns.png`** - Summary Infographic
    - High-level overview of SGNS
    - Core concept, key innovation, training process, and applications
    - Perfect for a quick reference or summary slide
    - **Use case**: Conclude SGNS section with a comprehensive overview
    - **Complexity**: Medium - brings together all SGNS concepts

## 🎓 Recommended Teaching Sequence

1. **Start with TF-IDF (visualizations 1-4)**: Students understand simpler, interpretable method first
2. **Show TF-IDF to SGNS comparison (visualization 4)**: Bridge between the two methods
3. **Move to SGNS (visualizations 5-11)**: Build on foundational understanding
4. **Reinforce with interactive code**: Run `python sgns.py` and `python classroom_examples.py`
   - **Use case**: Wrap-up or take-home overview

## Running the Code

### Generate Visualizations
```bash
python sgns_visualization.py
```
This will recreate all 7 visualization PNG files.

### Run the Core Implementation
```bash
python sgns.py
```
This demonstrates SGNS on a toy corpus and shows:
- How the model learns embeddings
- Finding similar words
- Understanding the algorithm details

## Classroom Teaching Sequence

**Option 1: Quick Overview (15 minutes)**
1. Show `07_infographic.png` - What is SGNS?
2. Show `01_context_window.png` - How does it look at text?
3. Show `02_sampling_process.png` - How does it train efficiently?
4. Show `03_embeddings_2d.png` - What does it learn?

**Option 2: Deep Dive (30-45 minutes)**
1. Start with `07_infographic.png` for context
2. Use `01_context_window.png` to explain the sliding window
3. Detail `05_algorithm_steps.png` step-by-step
4. Explain `02_sampling_process.png` with math
5. Show `06_training_dynamics.png` to demonstrate learning
6. Analyze `04_similarity_heatmap.png` for quantitative results
7. End with `03_embeddings_2d.png` for visualization

**Option 3: Interactive Demo (1 hour)**
1. Show all visualizations as above
2. Run `python sgns.py` to demonstrate training
3. Experiment with parameters (embedding_dim, learning_rate, negative_samples)
4. Show how parameters affect learning

## Key Concepts Explained

### Why Skip-gram?
- "Skip" = skip the target word, predict context
- "Gram" = n-gram (context window)
- Learn word meanings from context

### Why Negative Sampling?
- **Problem**: Softmax over 1M+ vocabulary words is expensive
- **Solution**: Sample 1 positive word (true context) + k negative words (random)
- **Benefit**: 100x+ faster training (O(k) instead of O(V))

### Why It Works
1. Words appearing in similar contexts have similar meanings
2. Neural networks learn efficient representations through gradient descent
3. Negative sampling provides contrastive learning (maximize vs. minimize)

## Technical Details

- **Embedding dimension**: 50-300 (higher = more expressive but slower)
- **Context window**: typically 2-10 (larger = more context)
- **Negative samples**: typically 5-20 (more = more stable but slower)
- **Learning rate**: typically 0.01-0.1
- **Epochs**: typically 5-20 (more = better convergence but diminishing returns)

## Python Implementation Files

- **`sgns.py`**: Full implementation of SGNS algorithm with comments
- **`sgns_visualization.py`**: Generates all classroom visualizations

## Dependencies

- NumPy: Matrix operations
- Matplotlib: Plotting
- Scikit-learn: t-SNE dimensionality reduction
- Seaborn: Statistical visualization

## Further Reading

- Original paper: "Distributed Representations of Words and Phrases and their Compositionality" (Mikolov et al., 2013)
- Related: Word2vec, FastText, GloVe
- Modern alternatives: BERT, GPT embeddings (Transformers)

---

**Created for classroom teaching - feel free to modify visualizations as needed!**
