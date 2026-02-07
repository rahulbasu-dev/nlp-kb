# 📚 Interactive NLP Educational Tool

A comprehensive teaching resource for Natural Language Processing, featuring **interactive web-based visualizations**, Python implementations, and educational materials for Skip-gram with Negative Sampling (SGNS), TF-IDF, and Neural Networks.

## 🌟 **[View Live Interactive Tool](https://rahulbasu-dev.github.io/nlp-kb/nlp_guide_index.html)**

Perfect for students learning NLP concepts through hands-on visualization!

---

## 🌐 Interactive Web Tool (NEW!)

### Features:
- **Neural Networks Visual Guide**
  - Animated forward/backward propagation
  - Interactive XOR problem solver
  - Activation functions explorer (Sigmoid, Tanh, ReLU, Leaky ReLU)
  - Real-time training playground

- **Word Embeddings Comparison**
  - Side-by-side comparison of TF-IDF, Word2Vec, CBOW, GloVe
  - Interactive visualizations and examples
  - Same dataset across all methods for direct comparison

- **Educational Pages**
  - Complete guides for each NLP method
  - Mathematical formulas with MathJax
  - Python code examples
  - Step-by-step calculations

### Access:
- **Live Site**: [https://rahulbasu-dev.github.io/nlp-kb/nlp_guide_index.html](https://rahulbasu-dev.github.io/nlp-kb/nlp_guide_index.html)
- **No installation needed** - runs entirely in browser
- **Works on mobile** and desktop

### Sharing with Students:
See **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** for detailed instructions on sharing this tool.

---

## 📦 Package Contents

### Core Implementation
- **`sgns.py`** (425 lines)
  - Full SGNS implementation from scratch with detailed comments
  - TF-IDF class for comparison
  - **Interactive menu system** with 4 demonstration options
  - Run: `python sgns.py` and select from menu

### Visualizations (11 educational graphics)

**TF-IDF Visualizations (4 PNG files - teach first):**
- **`01_tfidf_matrix.png`** - Document-term TF-IDF matrix heatmap
- **`02_idf_distribution.png`** - Word importance by IDF distribution
- **`03_tfidf_similarities.png`** - Document similarity comparison
- **`04_sgns_vs_tfidf_comparison.png`** - Side-by-side method comparison

**Skip-gram Visualizations (7 PNG files - teach after TF-IDF):**
- **`05_context_window.png`** - Sliding window mechanism over text
- **`06_sampling_process.png`** - Positive vs negative sampling explanation
- **`07_embeddings_2d.png`** - Word space visualization (t-SNE projection)
- **`08_similarity_heatmap.png`** - Word-to-word similarity matrix
- **`09_algorithm_steps.png`** - Step-by-step algorithm flow diagram
- **`10_training_dynamics.png`** - Learning progression (1→5→10→20 epochs)
- **`11_infographic_sgns.png`** - SGNS summary infographic

### Documentation
- **`VISUALIZATION_GUIDE.md`** - How to use each visualization
- **`TEACHING_CHEATSHEET.md`** - Quick reference for instructors (includes TF-IDF section)
- **`README.md`** (this file) - Overview

### Interactive Examples
- **`classroom_examples.py`** - 9 interactive demonstrations
  - Examples 1-7: SGNS-focused lessons
  - Example 8: TF-IDF basics
  - Example 9: SGNS vs TF-IDF comparison
  - Run: `python classroom_examples.py`

### Visualization Generator
- **`sgns_visualization.py`** - Creates all PNG visualizations
  - Run: `python sgns_visualization.py`

## 🚀 Quick Start

### For Classroom Use (30 minutes - Interactive Menu)
```bash
python sgns.py
# Then select from menu:
#   1. SGNS Only - See semantic embeddings in action
#   2. TF-IDF Only - See statistical approach to word importance
#   3. SGNS vs TF-IDF - Direct side-by-side comparison
#   4. Run All - Complete tour of both approaches
```

### For Interactive Teaching (1 hour)
```bash
# Terminal 1: Run the main implementation
python sgns.py

# Terminal 2: Run interactive examples  
python classroom_examples.py

# Browser/Presentation: Show the PNG visualizations
```

### For Students (2+ hours)
```bash
# Run everything
python sgns.py                    # Understand the algorithm
python classroom_examples.py      # Experiment with parameters
python sgns_visualization.py      # Generate and inspect visualizations
```

## 📚 Teaching Approaches

### Approach 1: Visualization-First (Best for Visual Learners)
1. Show `07_infographic.png` - What is SGNS?
2. Show `01_context_window.png` - How does the window work?
3. Show `02_sampling_process.png` - Why is it efficient?
4. Show `03_embeddings_2d.png` - What does it learn?
5. Run `sgns.py` - Live demonstration

**Time: 20-30 minutes**

### Approach 2: Algorithm-First (Best for Technical Learners)
1. Show `07_infographic.png` - Overview
2. Detail `05_algorithm_steps.png` - Step by step
3. Explain math with `TEACHING_CHEATSHEET.md`
4. Run `classroom_examples.py` - Example 6 (math behind training)
5. Show `03_embeddings_2d.png` - What emerged from the algorithm

**Time: 45-60 minutes**

### Approach 3: Interactive Deep Dive (Best for Hands-On Learning)
1. Brief intro with `07_infographic.png`
2. Run `classroom_examples.py` example by example
3. Pause to discuss visualizations between examples
4. Have students modify code and observe effects

**Time: 60-90 minutes**

## 🎓 Learning Outcomes

After this module, students should understand:

✓ **Conceptually**
- Words appearing in similar contexts have similar meanings
- How neural networks learn representations via gradient descent
- Why negative sampling is clever and efficient

✓ **Technically**  
- How context windows slide over text
- Positive vs negative sampling strategy
- Computing similarity (dot product, sigmoid, gradients)
- Why embedding vectors are useful

✓ **Practically**
- How to train an embedding model
- How to use embeddings for downstream tasks
- How to tune hyperparameters
- Why SGNS is important in NLP history

## 📊 Visualization Quick Reference

| Problem | Solution |
|---------|----------|
| "What is the context window?" | Show `01_context_window.png` |
| "Why is negative sampling better?" | Show `02_sampling_process.png` + math |
| "What does the model learn?" | Show `03_embeddings_2d.png` |
| "Can you quantify the relationships?" | Show `04_similarity_heatmap.png` |
| "Walk me through the algorithm" | Show `05_algorithm_steps.png` |
| "How does it improve over epochs?" | Show `06_training_dynamics.png` |
| "Give me the TL;DR" | Show `07_infographic.png` |

## 💾 File Sizes

```
sgns.py (11 KB)                    - Clean, commented implementation
sgns_visualization.py (17 KB)      - Visualization generation script
classroom_examples.py (13 KB)      - Interactive demonstrations
*.png files (800 KB total)         - 7 high-resolution visualizations
*.md files (25 KB total)           - Documentation
```

**Total package: ~850 KB** (entirely self-contained, no dependencies except NumPy, Matplotlib, scikit-learn)

## 🔧 System Requirements

- Python 3.7+
- NumPy (matrix operations)
- Matplotlib (plotting)
- scikit-learn (t-SNE for dimensionality reduction)
- Seaborn (statistical visualization)

All can be installed with:
```bash
pip install numpy matplotlib scikit-learn seaborn
```

## 📖 Background Reading

**Original Paper**
- Mikolov et al. (2013): "Distributed Representations of Words and Phrases and their Compositionality"
- https://arxiv.org/abs/1310.4546

**Related**
- Word2Vec family of models
- GloVe (alternative approach)
- FastText (extension with subword information)
- Transformers/BERT (modern successor)

## ✨ Key Features

- ✅ **Self-contained**: No external dependencies except standard ML libraries
- ✅ **Educational**: Heavy comments, clear variable names
- ✅ **Practical**: Runnable examples that work immediately
- ✅ **Visual**: 7 high-quality diagrams for presentations
- ✅ **Interactive**: Hands-on examples to experiment with
- ✅ **Flexible**: Works for 15-min overview or 2-hour deep dive

## 🎯 Use Cases

- **Lectures**: Show visualizations, run demonstrations
- **Tutorials**: Students work through code and examples
- **Research**: Foundation for exploring word embeddings
- **Portfolio**: Demonstrate understanding of NLP fundamentals
- **Competitions**: Baseline approach for embedding-based tasks

## 📝 Notes for Instructors

1. **Pre-class**: Run `sgns.py` once to verify everything works
2. **Demo**: Have `sgns.py` output ready to show
3. **Visuals**: Load PNG files in your presentation software
4. **Timing**: ~5 min per section, total 30-60 minutes
5. **Hands-on**: Give `classroom_examples.py` to students before class

## 🤝 Customization Ideas

- Modify corpus in `sgns.py` to use domain-specific text
- Experiment with hyperparameters in `classroom_examples.py`
- Create new visualizations by modifying `sgns_visualization.py`
- Add new examples to `classroom_examples.py`
- Combine with other embedding models (GloVe, FastText) for comparison

## 📞 Troubleshooting

| Issue | Solution |
|-------|----------|
| Import errors | `pip install -r requirements.txt` |
| Slow visualization generation | Normal - t-SNE takes time, set perplexity lower |
| Missing font glyphs | Harmless warnings, visualizations still display |
| Low accuracy on custom corpus | Use larger corpus, more epochs, tune learning_rate |

## 📄 License & Attribution

This package is created for educational purposes. It implements the algorithm from:
- Mikolov et al. (2013) - Original research

Feel free to:
- ✅ Use in teaching
- ✅ Share with students  
- ✅ Modify for your needs
- ✅ Create derivative works

## 🌟 What's Special About This Package

Unlike many tutorials, this includes:
1. **Working, tested code** - not pseudocode
2. **Rich visualizations** - for different learning styles
3. **Interactive examples** - hands-on experimentation
4. **Complete explanations** - from high level to mathematical details
5. **Flexible pacing** - works for 30-min overview or 2-hour deep dive

Perfect for:
- 👨‍🎓 Students learning NLP
- 👨‍🏫 Instructors teaching word embeddings
- 📊 Data scientists brushing up on foundations
- 🏆 Interview preparation (explain SGNS clearly!)

---

**Ready for the classroom! 🎓**

For questions or improvements, feel free to modify and experiment!
