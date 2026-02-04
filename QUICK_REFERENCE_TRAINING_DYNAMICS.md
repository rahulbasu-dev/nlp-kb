# 🎬 SGNS Training Dynamics - Quick Reference

## Access
- **URL:** http://localhost:5000/demo/sgns-training-dynamics
- **Navigation:** Home → Demos → 🎬 Training Dynamics

## What It Shows

### Animation 🎬
**Watch vectors move in 2D space during training**
- Similar words converge → appear near each other
- Negative samples pushed away → separate
- Frame-by-frame or smooth playback
- Use PCA for global view, t-SNE for clusters

### Distance 📉
**Line chart of word pair distances over epochs**
- See convergence behavior
- Flat lines = stable
- Drops = learning
- Compare multiple word pairs

### Heatmap 🔥
**Similarity matrix evolution**
- Red = similar words (getting more similar)
- Blue = dissimilar words (getting more different)
- Watch blocks form
- Shows semantic structure emerging

---

## Configuration

### Must Change
| Setting | Values | Default |
|---------|--------|---------|
| **Corpus** | Your text | Example |
| **Epochs** | 1-50 | 10 |

### Nice to Adjust
| Setting | Values | Default |
|---------|--------|---------|
| **Embedding Dim** | 2-200 | 30 |
| **Window Size** | 1-5 | 2 |
| **Method** | PCA / t-SNE / UMAP | PCA |
| **Viz Type** | Animation / Distance / Heatmap | Animation |

### Optional
| Setting | Values | Default |
|---------|--------|---------|
| **Negative Samples** | 1-20 | 5 |
| **Capture Interval** | 1-10 | 1 |

---

## Example Corpora

### Animals
```
the cat sat on the mat
the dog sat on the floor
the bird flew in the sky
the cat and dog are friends
```
→ **Expect:** cat/dog cluster, bird separate, sat/flew separate

### Fruits
```
apple is a red fruit
orange is a citrus fruit
banana is a yellow fruit
grapes grow on vines
```
→ **Expect:** apple/orange/banana cluster, grapes separate

### Simple
```
a b c
b c a
c a b
```
→ **Expect:** All three cluster (appear together in each sentence)

---

## Experiments to Try

### Experiment 1: Minimum Viable
- Corpus: "a b c d e"
- Epochs: 3
- Result: Quick, see basic convergence

### Experiment 2: Window Size Effect
- Run with window=1, then window=5
- Same corpus
- Compare: How much does context matter?

### Experiment 3: Method Comparison
- Generate with PCA
- Re-run with t-SNE
- Note: Different patterns visible?

### Experiment 4: Your Data
- Use sentences from a book you like
- Watch the character names/actions cluster
- See what the model learns about your text

---

## What to Look For

### In Animation
✓ Increasing structure over time
✓ Similar words moving together
✓ Stabilization after several epochs
✓ Random → organized progression

### In Distance Chart
✓ Generally decreasing curves
✓ Plateauing (convergence)
✓ Early drops (fast learning)
✓ Different rates for different pairs

### In Heatmap
✓ Red blocks along diagonal
✓ Gradual emergence from gray
✓ Block structure (similar words near each other)
✓ Clear separation of unrelated words

---

## Common Questions

**Q: Why do I see mostly gray in the heatmap early on?**
A: Random initialization → vectors are near-orthogonal → low similarity

**Q: Should I use more epochs?**
A: Usually 5-20 sufficient. More epochs = slower but more stable.

**Q: Which method should I use?**
A: PCA (default) is fast. t-SNE shows clusters better. UMAP is balanced.

**Q: Can I see individual word trajectories?**
A: Not yet, but you can pause and examine positions at each epoch.

**Q: What if my corpus is very small?**
A: It still works! May show less structure with fewer unique words.

**Q: Why do some words barely move?**
A: They may have appeared in very similar contexts from the start.

---

## Parameters Explained

### Embedding Dimension
- **Small (2-10):** Fast, simple structure
- **Medium (30):** Good balance
- **Large (100+):** Complex, needs more training

### Window Size
- **1:** Very local context only
- **2-3:** Good for most text
- **5+:** Broader context, less specific relationships

### Negative Samples
- **1-3:** Quick training, less learning
- **5:** Default, good balance
- **10+:** More training, slower

### Epochs
- **1-3:** See initial structure
- **5-10:** Convergence visible
- **20+:** Stable, risk of over-training

### Method
- **PCA:** Fast, go with this
- **t-SNE:** Better clusters, slower
- **UMAP:** New, good balance

---

## Keyboard Shortcuts

| Action | How |
|--------|-----|
| Play animation | Click ▶️ button |
| Pause animation | Click ⏸ button |
| Jump to epoch | Use slider |
| Zoom in chart | Scroll or box select |
| Pan chart | Click and drag |
| Reset zoom | Double-click |

---

## Tips for Teachers

1. **Show in lectures:** Pause and discuss at key moments
2. **Ask predictions:** "What will happen next?"
3. **Compare settings:** Run twice with different parameters
4. **Highlight patterns:** "Notice how these words clustered?"
5. **Connect to theory:** "This is negative sampling in action"

---

## Tips for Students

1. **Start simple:** Use default corpus first
2. **Change one thing:** Only adjust one parameter at a time
3. **Watch carefully:** Pause and examine positions
4. **Take notes:** Write what you observe
5. **Experiment:** Try different corpora
6. **Predict first:** Before clicking generate, predict what you'll see

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No valid sentences" | Check corpus has actual words |
| Chart doesn't show | Refresh page, try PCA method |
| Very slow | Reduce epochs, use PCA |
| Empty heatmap | Need more similar words in corpus |

---

## Related Topics

- **Word2Vec:** Similar approach, different implementation
- **GloVe:** Combines local + global context
- **FastText:** Handles subwords
- **BERT:** Modern transformer-based embeddings
- **Dimensionality Reduction:** Why PCA/t-SNE needed for visualization

---

## File Locations

| File | Purpose |
|------|---------|
| `training_dynamics.py` | Core visualization logic |
| `demo_sgns_dynamics.html` | Web UI |
| `app.py` | Flask endpoint |
| `TRAINING_DYNAMICS_GUIDE.md` | Full documentation |

---

## Success Checklist

- [ ] Server running: `python app.py`
- [ ] Can access: http://localhost:5000
- [ ] Found link: Demos → 🎬 Training Dynamics
- [ ] Page loads: "Configuration" + "Visualization" panels visible
- [ ] Generated visualization: No errors
- [ ] Animation plays: Can click ▶️ and see vectors move
- [ ] Metadata displays: Vocab size, epochs, method shown
- [ ] Everything works: Ready to explore!

---

**Created:** January 24, 2026
**Version:** 1.0
**Status:** ✅ Ready to Use

🎬 **Ready to watch embeddings learn!**
