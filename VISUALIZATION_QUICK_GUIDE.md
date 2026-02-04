# 📊 Vector Embedding Visualizations - Quick Reference Guide

## What Are Vector Embeddings?

Vectors are lists of numbers that represent words or documents. Embeddings map these high-dimensional numbers (50-300D) to 2D space so we can visualize them.

```
Word "cat" (50D)     PCA        Position on Chart
[0.2, -0.5, 0.1, → Reduction → (x: 2.3, y: -1.5)
 0.3, 0.0, ...]     Algorithm
```

## Quick Start

### For TF-IDF Visualization
1. Go to: `http://localhost:5000/demo/tfidf`
2. Enter 3+ documents (or click "Load This Example")
3. Click "Calculate TF-IDF"
4. **See the 2D chart showing document positions!**

### For SGNS Visualization
1. Go to: `http://localhost:5000/demo/sgns`
2. Enter 3+ sentences or click "Load This Example"
3. Click "Train Model"
4. **See the 2D chart showing word positions!**

## What Do The Charts Show?

### TF-IDF Chart (Documents)
```
         Document A
            •
           / \
          /   \
         /     \ Document B
        •       •
            
       Document C

Interpretation:
• Nearby documents = Similar word content
• Far documents = Different vocabulary
• Clusters = Documents on similar topics
```

### SGNS Chart (Words)
```
    dog  •  cat
         •
    fox •
    
    the  •  in
        on •
    
Interpretation:
• Nearby words = Similar context in corpus
• "dog", "cat", "fox" close = semantic similarity
• "the", "in", "on" close = grammatical similarity
```

## Features

### 🎯 Interactive Controls
- **Hover**: See full text/word information
- **Zoom**: Magnify areas of interest (scroll wheel)
- **Pan**: Drag to move around chart
- **Reset**: Double-click to reset view
- **Download**: Camera icon → Save as PNG

### 🎨 Chart Elements
- **Dots**: Each point is a document or word
- **Labels**: Text name of each point
- **Color**: Gradient shows distance from origin
- **Grid**: Reference for coordinates

### 📊 Metadata Shown
- **For TF-IDF**: 
  - Number of documents
  - Vocabulary size (unique words)
  - Reduction method (PCA)

- **For SGNS**:
  - Vocabulary size (words learned)
  - Embedding dimension (50D, 100D, etc.)
  - Reduction method (PCA)

## How To Interpret Results

### TF-IDF Interpretation
```
High scores (upper right)
- Important words for document
- Uncommon across corpus
- Topic-specific terminology

Low scores (lower left)
- Common words (the, a, is)
- Stop words
- Generic language
```

### SGNS Interpretation
```
Clustered together
- Words share context
- Semantically related
- Appear in similar sentences

Isolated points
- Unique context
- Rare word patterns
- Specialized vocabulary
```

## Comparison

| Feature | TF-IDF | SGNS |
|---------|--------|------|
| **What it shows** | Document similarity | Word similarity |
| **Based on** | Word frequency | Context window |
| **Best for** | Finding similar documents | Finding similar words |
| **Speed** | Very fast | Slower (training) |
| **Interpretability** | Frequency-based | Semantic-based |

## Common Questions

### Q: Why are some documents very close?
**A**: They share similar important words. They cover similar topics.

### Q: Why is a word isolated?
**A**: It appears in unique contexts different from other words.

### Q: Can I change the reduction method?
**A**: Currently uses PCA (fast & stable). t-SNE and UMAP available in code.

### Q: What if chart is hard to see?
**A**: Click and drag to zoom in on areas of interest.

### Q: Do I need many documents for good visualization?
**A**: 3-5 minimum works. More data = better clustering patterns.

### Q: Can I download the chart?
**A**: Yes! Click the camera icon in Plotly toolbar.

## Technical Details

### Dimensionality Reduction Methods

#### PCA (Default - Always Available)
```
Pros:
✓ Very fast
✓ Deterministic
✓ Preserves global structure
✓ No parameters to tune

Cons:
✗ May miss local clusters
✗ Works best with high-dimensional data
```

#### t-SNE (Optional)
```
Pros:
✓ Better local structure
✓ Great for finding clusters
✓ Handles non-linear manifolds

Cons:
✗ Slower (~200ms)
✗ Non-deterministic
✗ Needs perplexity tuning
```

#### UMAP (Optional)
```
Pros:
✓ Faster than t-SNE
✓ Balance of structure preservation
✓ Preserves topology

Cons:
✗ Requires installation
✗ Non-deterministic
```

## Tips for Best Results

### For TF-IDF Visualization
1. **Use diverse documents** - Too similar docs will cluster together
2. **Include enough text** - Short documents don't show patterns well
3. **Avoid common words only** - Use specific, topic-relevant words
4. **Try 3-5 documents first** - Easy to see patterns

### For SGNS Visualization
1. **Use more sentences** - Richer context patterns emerge
2. **Related vocabulary** - Sentences about same topic cluster better
3. **Vary sentence structure** - Different contexts reveal word relationships
4. **Train longer** - More epochs → better embeddings (10-20 recommended)

## Sample Data To Try

### TF-IDF Example - Animals
```
Doc 1: "The cat sat on the mat"
Doc 2: "The dog played in the park"
Doc 3: "The bird flew over trees"
```
→ See how documents cluster by subject

### TF-IDF Example - Technology
```
Doc 1: "Machine learning uses neural networks"
Doc 2: "Natural language processing helps text analysis"
Doc 3: "Computer vision processes images"
```
→ See how NLP docs differ from others

### SGNS Example - Animals
```
"the cat sat on the mat"
"the dog played in the park"
"the bird flew in the sky"
```
→ See animals (cat, dog, bird) cluster together
→ See positions (on, in) cluster together

## Troubleshooting

### Chart doesn't appear
- Ensure JavaScript is enabled
- Check browser console for errors
- Try refreshing the page

### Chart is empty
- Make sure you entered data
- Try clicking "Load This Example"
- Check for error messages

### Visualization seems wrong
- Try with more data
- Ensure data quality (no empty fields)
- Try clicking "Reset View"

### Very slow performance
- Reduce number of documents/words
- Use shorter corpus
- Try PCA method (default)

## Advanced Features

### Via Python API
```python
from embeddings_viz import visualize_tfidf_vectors, reduce_to_2d

# Reduce with different methods
points_2d = reduce_to_2d(vectors, method='pca')      # Fast
points_2d = reduce_to_2d(vectors, method='tsne')     # Better clusters
points_2d = reduce_to_2d(vectors, method='umap')     # Balanced
```

### Custom Parameters (SGNS)
```javascript
runSGNSDemo() uses default parameters:
- Embedding Dim: 50 (change in UI: 10-300)
- Window Size: 2 (change in UI: 1-10)
- Negative Samples: 5 (change in UI: 1-20)
- Epochs: 10 (change in UI: 1-100)

Higher dimensions → Richer representations
More epochs → Better training → Better embeddings
```

## Learning Resources

- 📚 **What are word embeddings?**
  https://en.wikipedia.org/wiki/Word2vec

- 📚 **TF-IDF Explained**
  https://en.wikipedia.org/wiki/Tf%E2%80%93idf

- 📚 **PCA Visualization**
  https://en.wikipedia.org/wiki/Principal_component_analysis

- 📚 **t-SNE Visualization**
  https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding

## Summary

✅ **You can now:**
- Visualize document similarity (TF-IDF)
- Visualize word relationships (SGNS)
- See embeddings in 2D space
- Interact with charts (zoom, pan, hover)
- Download visualizations
- Understand high-dimensional data intuitively

**Key Takeaway**: Nearby items in 2D space = Similar in high-dimensional space!

---

**Last Updated**: January 24, 2026
**Status**: ✅ Ready to Use
