"""
Skip-gram with Negative Sampling - Visualization for Teaching

Creates multiple visualizations to explain SGNS and TF-IDF concepts:
1. Context window sliding mechanism
2. Positive vs negative sampling process
3. Word embeddings in 2D space (using t-SNE)
4. Similarity between word pairs
5. Training dynamics over epochs
6. TF-IDF document-term matrix
7. IDF distribution (term importance)
8. TF-IDF document similarities
9. SGNS vs TF-IDF comparison
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from sklearn.manifold import TSNE
import seaborn as sns
from sgns import SkipGramNegativeSampling, TFIDF

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10


def visualize_context_window():
    """Visualize how the context window slides over a sentence."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle('Skip-gram: Context Window Mechanism', fontsize=16, fontweight='bold')
    
    sentence = ["king", "is", "a", "powerful", "ruler"]
    window_size = 2
    
    positions = [0, 1, 2, 3]
    
    for plot_idx, target_pos in enumerate(positions):
        ax = axes.flatten()[plot_idx]
        
        # Draw words
        x_positions = range(len(sentence))
        colors = []
        for i, word in enumerate(sentence):
            if i == target_pos:
                colors.append('red')  # Target word
            elif abs(i - target_pos) <= window_size and i != target_pos:
                colors.append('green')  # Context words
            else:
                colors.append('gray')  # Outside window
        
        ax.barh(x_positions, [1]*len(sentence), color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        ax.set_yticks(x_positions)
        ax.set_yticklabels(sentence)
        ax.set_xlim(-0.5, 1.5)
        ax.set_xticks([])
        ax.set_title(f'Target: "{sentence[target_pos]}" (Position {target_pos})', fontsize=11, fontweight='bold')
        
        # Add legend
        if plot_idx == 0:
            ax.text(1.15, 4.5, '🔴 Target', fontsize=10, color='red', fontweight='bold')
            ax.text(1.15, 3.8, '🟢 Context', fontsize=10, color='green', fontweight='bold')
            ax.text(1.15, 3.1, '⚫ Outside', fontsize=10, color='gray', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('05_context_window.png', dpi=150, bbox_inches='tight')
    print("[OK] Saved: 05_context_window.png")
    plt.close()


def visualize_sampling_process():
    """Visualize positive sampling vs negative sampling."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Skip-gram: Positive vs Negative Sampling', fontsize=16, fontweight='bold')
    
    # Left: Positive sampling
    ax = axes[0]
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    
    # Target word vector
    target = np.array([0, 0])
    ax.arrow(0, 0, 1, 0.5, head_width=0.15, head_length=0.1, fc='red', ec='red', linewidth=3, label='Target word')
    
    # Positive context word (close)
    pos = np.array([0.9, 0.4])
    ax.arrow(0, 0, pos[0], pos[1], head_width=0.15, head_length=0.1, fc='green', ec='green', linewidth=3, alpha=0.7, label='Context word')
    ax.plot(pos[0], pos[1], 'go', markersize=15, alpha=0.7)
    
    # Maximize dot product
    dot_prod = np.dot([1, 0.5], pos)
    ax.text(0.5, 1.3, f'Objective: Maximize\ndot product = {dot_prod:.2f}', 
            fontsize=12, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8), fontweight='bold')
    
    ax.set_title('Positive Sampling: Maximize Similarity', fontsize=13, fontweight='bold')
    ax.set_xlabel('Dimension 1')
    ax.set_ylabel('Dimension 2')
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Right: Negative sampling
    ax = axes[1]
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_aspect('equal')
    
    # Target word vector
    ax.arrow(0, 0, 1, 0.5, head_width=0.15, head_length=0.1, fc='red', ec='red', linewidth=3, label='Target word')
    
    # Negative samples (far away)
    negatives = [
        np.array([-1.2, 0.8]),
        np.array([0.3, -1.4]),
        np.array([-0.8, -1.1])
    ]
    
    for i, neg in enumerate(negatives):
        ax.arrow(0, 0, neg[0], neg[1], head_width=0.15, head_length=0.1, fc='blue', ec='blue', linewidth=2, alpha=0.5)
        ax.plot(neg[0], neg[1], 'bx', markersize=15, markeredgewidth=3, alpha=0.7)
    
    ax.text(0.2, -1.8, 'Objective: Minimize\ndot products with negatives', 
            fontsize=12, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8), fontweight='bold')
    
    ax.set_title('Negative Sampling: Minimize Similarity', fontsize=13, fontweight='bold')
    ax.set_xlabel('Dimension 1')
    ax.set_ylabel('Dimension 2')
    ax.grid(True, alpha=0.3)
    
    # Add shared legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', label='Target word vector'),
        Patch(facecolor='green', label='Positive context word'),
        Patch(facecolor='blue', label='Negative samples')
    ]
    fig.legend(handles=legend_elements, loc='upper center', ncol=3, fontsize=11, bbox_to_anchor=(0.5, 0.98))
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('02_sampling_process.png', dpi=150, bbox_inches='tight')
    print("[OK] Saved: 06_sampling_process.png")
    plt.close()


def visualize_word_embeddings():
    """Train model and visualize word embeddings in 2D using t-SNE."""
    print("\nTraining model for embedding visualization...")
    
    # Corpus
    sentences = [
        ["king", "is", "a", "man"],
        ["queen", "is", "a", "woman"],
        ["prince", "is", "a", "boy"],
        ["princess", "is", "a", "girl"],
        ["king", "and", "queen", "rule", "the", "kingdom"],
        ["man", "and", "woman", "walked", "in", "the", "park"],
        ["boy", "and", "girl", "played", "in", "the", "garden"],
    ]
    
    # Train
    model = SkipGramNegativeSampling(embedding_dim=50, learning_rate=0.025, 
                                     negative_samples=5, window_size=2)
    model.build_vocab(sentences)
    model.train(sentences, epochs=15)
    
    # Get embeddings
    vocab_words = sorted(model.vocab.keys())
    embeddings = np.array([model.get_vector(word) for word in vocab_words])
    
    # Reduce to 2D using t-SNE
    print("Reducing dimensionality with t-SNE...")
    tsne = TSNE(n_components=2, random_state=42, perplexity=3)
    embeddings_2d = tsne.fit_transform(embeddings)
    
    # Categorize words
    categories = {
        'Gender': ['man', 'woman', 'boy', 'girl', 'king', 'queen', 'prince', 'princess'],
        'Function': ['is', 'and', 'rule', 'walked', 'played'],
        'Object': ['kingdom', 'park', 'garden', 'a', 'the', 'in']
    }
    
    colors = {}
    for category, words in categories.items():
        for word in words:
            colors[word] = category
    
    color_map = {'Gender': '#FF6B6B', 'Function': '#4ECDC4', 'Object': '#FFE66D'}
    
    # Plot
    fig, ax = plt.subplots(figsize=(12, 9))
    
    for category in categories.keys():
        mask = [colors.get(w, None) == category for w in vocab_words]
        if any(mask):
            x = embeddings_2d[mask, 0]
            y = embeddings_2d[mask, 1]
            ax.scatter(x, y, s=300, alpha=0.7, c=color_map[category], 
                      label=category, edgecolors='black', linewidth=2)
    
    # Add word labels
    for i, word in enumerate(vocab_words):
        ax.annotate(word, (embeddings_2d[i, 0], embeddings_2d[i, 1]),
                   fontsize=11, fontweight='bold', ha='center', va='center')
    
    ax.set_xlabel('t-SNE Dimension 1', fontsize=12, fontweight='bold')
    ax.set_ylabel('t-SNE Dimension 2', fontsize=12, fontweight='bold')
    ax.set_title('Word Embeddings Space (t-SNE Projection)\nWords with similar meanings cluster together', 
                fontsize=14, fontweight='bold', pad=20)
    ax.legend(fontsize=12, loc='best', title='Word Category', title_fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('07_embeddings_2d.png', dpi=150, bbox_inches='tight')
    print("[OK] Saved: 07_embeddings_2d.png")
    plt.close()
    
    return model


def visualize_similarity_heatmap(model):
    """Show similarity between words as a heatmap."""
    test_words = ['king', 'queen', 'man', 'woman', 'prince', 'princess', 'boy', 'girl', 'is', 'rule']
    
    # Compute similarities
    n = len(test_words)
    similarity_matrix = np.zeros((n, n))
    
    for i, word1 in enumerate(test_words):
        if word1 not in model.vocab:
            continue
        v1 = model.get_vector(word1)
        v1_norm = v1 / (np.linalg.norm(v1) + 1e-10)
        
        for j, word2 in enumerate(test_words):
            if word2 not in model.vocab:
                continue
            v2 = model.get_vector(word2)
            v2_norm = v2 / (np.linalg.norm(v2) + 1e-10)
            
            similarity_matrix[i, j] = np.dot(v1_norm, v2_norm)
    
    # Plot heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(similarity_matrix, annot=True, fmt='.2f', cmap='RdYlGn', center=0,
               xticklabels=test_words, yticklabels=test_words, cbar_kws={'label': 'Cosine Similarity'},
               ax=ax, vmin=-0.5, vmax=1, linewidths=0.5, annot_kws={'fontsize': 9})
    
    ax.set_title('Word Similarity Matrix (Cosine Similarity)\nDiagonal is 1.0 (word with itself)', 
                fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    plt.savefig('08_similarity_heatmap.png', dpi=150, bbox_inches='tight')
    print("[OK] Saved: 08_similarity_heatmap.png")
    plt.close()


def visualize_algorithm_steps():
    """Visualize the SGNS algorithm steps."""
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.4, wspace=0.3)
    
    fig.suptitle('Skip-gram with Negative Sampling: Algorithm Flow', 
                fontsize=16, fontweight='bold', y=0.98)
    
    # Step 1: Input
    ax1 = fig.add_subplot(gs[0, :])
    ax1.text(0.5, 0.7, 'Step 1: Input Corpus', fontsize=13, fontweight='bold', ha='center',
            transform=ax1.transAxes)
    ax1.text(0.5, 0.4, 'Sentence: "king is a powerful ruler"', fontsize=12, ha='center',
            transform=ax1.transAxes, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    ax1.axis('off')
    
    # Step 2: Context Window
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.text(0.5, 0.95, 'Step 2: Slide Context Window', fontsize=12, fontweight='bold', 
            ha='center', transform=ax2.transAxes)
    
    words = ['king', 'is', 'a', 'powerful', 'ruler']
    y_pos = np.arange(len(words))
    colors_step2 = ['red', 'green', 'green', 'gray', 'gray']
    ax2.barh(y_pos, [1]*len(words), color=colors_step2, alpha=0.6, edgecolor='black', linewidth=1.5)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(words)
    ax2.set_xlim(0, 1.2)
    ax2.set_xticks([])
    ax2.text(1.08, 1.8, 'window=2', fontsize=10, fontweight='bold')
    
    # Step 3: Positive Sampling
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.text(0.5, 0.95, 'Step 3: Positive Sampling', fontsize=12, fontweight='bold', 
            ha='center', transform=ax3.transAxes)
    
    ax3.text(0.5, 0.65, 'Target: "a"', fontsize=11, fontweight='bold', ha='center',
            transform=ax3.transAxes, bbox=dict(boxstyle='round', facecolor='#FFE66D', alpha=0.7))
    ax3.text(0.5, 0.45, 'Context words:\n"is", "powerful"', fontsize=10, ha='center',
            transform=ax3.transAxes, bbox=dict(boxstyle='round', facecolor='#90EE90', alpha=0.7))
    ax3.text(0.5, 0.15, '✓ Maximize dot products', fontsize=10, ha='center', 
            transform=ax3.transAxes, color='darkgreen', fontweight='bold')
    ax3.axis('off')
    
    # Step 4: Negative Sampling
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.text(0.5, 0.95, 'Step 4: Negative Sampling', fontsize=12, fontweight='bold', 
            ha='center', transform=ax4.transAxes)
    
    ax4.text(0.5, 0.65, 'Sample k random words\n(based on frequency)', fontsize=11, ha='center',
            transform=ax4.transAxes, bbox=dict(boxstyle='round', facecolor='#87CEEB', alpha=0.7))
    ax4.text(0.5, 0.35, 'e.g., "king", "ruler", "the",\n"powerful", "garden"', fontsize=10, ha='center',
            transform=ax4.transAxes, bbox=dict(boxstyle='round', facecolor='#FFB6C1', alpha=0.7))
    ax4.text(0.5, 0.05, '✗ Minimize dot products', fontsize=10, ha='center', 
            transform=ax4.transAxes, color='darkred', fontweight='bold')
    ax4.axis('off')
    
    # Step 5: Update
    ax5 = fig.add_subplot(gs[2, 1])
    ax5.text(0.5, 0.95, 'Step 5: Update Embeddings', fontsize=12, fontweight='bold', 
            ha='center', transform=ax5.transAxes)
    
    ax5.text(0.5, 0.65, 'Gradient descent:\nv_new = v_old + lr × gradient', fontsize=10, ha='center',
            transform=ax5.transAxes, bbox=dict(boxstyle='round', facecolor='#DDA0DD', alpha=0.7))
    ax5.text(0.5, 0.25, 'Repeat for all words\nand epochs', fontsize=10, ha='center', style='italic',
            transform=ax5.transAxes, bbox=dict(boxstyle='round', facecolor='#F0E68C', alpha=0.7))
    ax5.axis('off')
    
    plt.savefig('09_algorithm_steps.png', dpi=150, bbox_inches='tight')
    print("[OK] Saved: 09_algorithm_steps.png")
    plt.close()


def visualize_training_dynamics():
    """Visualize how embeddings change during training."""
    print("\nVisualizing training dynamics...")
    
    sentences = [
        ["king", "is", "a", "man"],
        ["queen", "is", "a", "woman"],
        ["man", "and", "woman", "walked"],
    ]
    
    # Train multiple times with different epoch counts
    epochs_list = [1, 5, 10, 20]
    embeddings_list = []
    
    for epochs in epochs_list:
        model = SkipGramNegativeSampling(embedding_dim=30, learning_rate=0.025, 
                                         negative_samples=3, window_size=2)
        model.build_vocab(sentences)
        model.train(sentences, epochs=epochs)
        embeddings = np.array([model.get_vector(word) for word in sorted(model.vocab.keys())])
        embeddings_list.append(embeddings)
    
    # Reduce to 2D
    all_embeddings = np.vstack(embeddings_list)
    tsne = TSNE(n_components=2, random_state=42, perplexity=2)
    all_embeddings_2d = tsne.fit_transform(all_embeddings)
    
    vocab = sorted(model.vocab.keys())
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('Word Embeddings Evolution During Training', fontsize=16, fontweight='bold')
    
    for idx, (ax, epochs) in enumerate(zip(axes.flatten(), epochs_list)):
        embeddings_2d = all_embeddings_2d[idx*len(vocab):(idx+1)*len(vocab)]
        
        # Color by word type
        colors_map = {
            'king': '#FF6B6B', 'queen': '#FF6B6B',
            'man': '#4ECDC4', 'woman': '#4ECDC4',
            'is': '#FFE66D', 'a': '#FFE66D',
            'and': '#95E1D3', 'walked': '#95E1D3'
        }
        
        colors = [colors_map.get(w, '#CCCCCC') for w in vocab]
        
        ax.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], s=400, c=colors, 
                  alpha=0.7, edgecolors='black', linewidth=2)
        
        for i, word in enumerate(vocab):
            ax.annotate(word, (embeddings_2d[i, 0], embeddings_2d[i, 1]),
                       fontsize=10, fontweight='bold', ha='center', va='center')
        
        ax.set_title(f'After {epochs} Epoch{"s" if epochs > 1 else ""}', fontsize=12, fontweight='bold')
        ax.set_xlabel('Dimension 1')
        ax.set_ylabel('Dimension 2')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('10_training_dynamics.png', dpi=150, bbox_inches='tight')
    print("[OK] Saved: 10_training_dynamics.png")
    plt.close()


def create_infographic():
    """Create a summary infographic of SGNS."""
    fig = plt.figure(figsize=(14, 10))
    fig.patch.set_facecolor('white')
    
    # Title
    fig.text(0.5, 0.97, 'Skip-gram with Negative Sampling (SGNS)', 
            ha='center', fontsize=20, fontweight='bold')
    fig.text(0.5, 0.93, 'A Word Embedding Model That Learns From Context', 
            ha='center', fontsize=14, style='italic', color='gray')
    
    # Left side: Concept
    ax_left = plt.subplot(2, 2, 1)
    ax_left.text(0.05, 0.95, 'Core Concept:', fontsize=12, fontweight='bold', 
                transform=ax_left.transAxes)
    ax_left.text(0.05, 0.80, 'Words that appear\nin similar contexts\nshould have\nsimilar meanings', 
                fontsize=11, transform=ax_left.transAxes, 
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8, pad=1))
    ax_left.text(0.05, 0.40, 'Example:\n"king" and "queen"\nappear with similar\nwords like "throne",\n"rule", "powerful"', 
                fontsize=10, transform=ax_left.transAxes, style='italic',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8, pad=1))
    ax_left.axis('off')
    
    # Right side: Key innovation
    ax_right = plt.subplot(2, 2, 2)
    ax_right.text(0.05, 0.95, 'Key Innovation:', fontsize=12, fontweight='bold', 
                 transform=ax_right.transAxes)
    ax_right.text(0.05, 0.75, 'Negative Sampling', fontsize=11, fontweight='bold',
                 transform=ax_right.transAxes, color='darkred')
    ax_right.text(0.05, 0.60, 'Instead of computing\nsoftmax over entire\nvocabulary, sample just:\n\n• 1 positive word\n• k negative words', 
                fontsize=10, transform=ax_right.transAxes,
                bbox=dict(boxstyle='round', facecolor='#FFE6E6', alpha=0.8, pad=1))
    ax_right.text(0.05, 0.15, '⚡ 100x faster training!', fontsize=11, fontweight='bold',
                 transform=ax_right.transAxes, color='darkgreen',
                 bbox=dict(boxstyle='round', facecolor='#E6FFE6', alpha=0.8, pad=0.8))
    ax_right.axis('off')
    
    # Bottom left: Algorithm summary
    ax_bottom_left = plt.subplot(2, 2, 3)
    ax_bottom_left.text(0.5, 0.95, 'Training Process', fontsize=12, fontweight='bold', 
                       ha='center', transform=ax_bottom_left.transAxes)
    
    steps_text = """1. Slide a window over text
2. For each target word:
   • Get context words (positive)
   • Sample random words (negative)
   • Maximize similarity to context
   • Minimize similarity to negatives
3. Update word embeddings
4. Repeat over many epochs"""
    
    ax_bottom_left.text(0.05, 0.75, steps_text, fontsize=9, transform=ax_bottom_left.transAxes,
                       family='monospace', bbox=dict(boxstyle='round', facecolor='#F0F0F0', alpha=0.9, pad=1))
    ax_bottom_left.axis('off')
    
    # Bottom right: Applications
    ax_bottom_right = plt.subplot(2, 2, 4)
    ax_bottom_right.text(0.5, 0.95, 'Applications', fontsize=12, fontweight='bold', 
                        ha='center', transform=ax_bottom_right.transAxes)
    
    apps_text = """✓ Word similarities
✓ Analogies (king - man + woman = queen)
✓ Clustering documents
✓ Recommendation systems
✓ Feature engineering
✓ Transfer learning"""
    
    ax_bottom_right.text(0.05, 0.75, apps_text, fontsize=10, transform=ax_bottom_right.transAxes,
                        bbox=dict(boxstyle='round', facecolor='#E6F3FF', alpha=0.9, pad=1))
    ax_bottom_right.axis('off')
    
    plt.savefig('11_infographic_sgns.png', dpi=150, bbox_inches='tight')
    print("[OK] Saved: 11_infographic_sgns.png")
    plt.close()


def visualize_tfidf_matrix():
    """Visualize TF-IDF document-term matrix as heatmap."""
    # Create sample documents
    documents = [
        ["machine", "learning", "is", "powerful", "for", "predictions"],
        ["deep", "learning", "uses", "neural", "networks", "successfully"],
        ["machine", "learning", "and", "deep", "learning", "are", "related"],
    ]
    
    # Train TF-IDF
    tfidf = TFIDF()
    tfidf.fit(documents)
    
    # Get TF-IDF matrix
    matrix = []
    for doc in documents:
        vec = tfidf.transform(doc)
        matrix.append(vec)
    
    matrix = np.array(matrix)
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create heatmap
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
    
    # Set labels
    vocab_list = sorted(tfidf.vocab.keys(), key=lambda x: tfidf.vocab[x])
    doc_labels = [f'Doc {i+1}' for i in range(len(documents))]
    
    ax.set_xticks(range(len(vocab_list)))
    ax.set_yticks(range(len(documents)))
    ax.set_xticklabels(vocab_list, rotation=45, ha='right')
    ax.set_yticklabels(doc_labels)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('TF-IDF Score', rotation=270, labelpad=20)
    
    # Add title
    ax.set_title('TF-IDF Document-Term Matrix\n(Importance of each word in each document)', 
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Words', fontsize=12)
    ax.set_ylabel('Documents', fontsize=12)
    
    # Add text annotations
    for i in range(len(documents)):
        for j in range(len(vocab_list)):
            text = ax.text(j, i, f'{matrix[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=8)
    
    plt.tight_layout()
    plt.savefig('01_tfidf_matrix.png', dpi=150, bbox_inches='tight')
    print("[OK] Saved: 01_tfidf_matrix.png")
    plt.close()


def visualize_idf_distribution():
    """Visualize IDF (Inverse Document Frequency) values."""
    # Create sample documents
    documents = [
        ["the", "cat", "sat", "on", "the", "mat"],
        ["a", "dog", "sat", "on", "the", "floor"],
        ["the", "cat", "and", "dog", "play", "together"],
    ]
    
    # Train TF-IDF to compute IDF
    tfidf = TFIDF()
    tfidf.fit(documents)
    
    # Get IDF values
    words = sorted(tfidf.vocab.keys(), key=lambda x: tfidf.idf.get(x, 0), reverse=True)
    idf_values = [tfidf.idf.get(word, 0) for word in words]
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Bar chart of IDF values
    colors = ['green' if v > 0.5 else 'orange' if v > 0.2 else 'red' for v in idf_values]
    bars = ax1.barh(words, idf_values, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax1.set_xlabel('IDF (Inverse Document Frequency)', fontsize=12, fontweight='bold')
    ax1.set_title('Word Importance by IDF\n(Higher = appears in fewer documents)', 
                 fontsize=13, fontweight='bold')
    ax1.axvline(x=0.5, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Rare threshold')
    ax1.legend()
    
    # Right: Explanation
    ax2.axis('off')
    explanation = """
IDF Formula:
IDF(word) = log(total_docs / docs_with_word)

🔴 Red bars: Common words (low IDF)
   - Appear in most documents
   - Less discriminative
   
🟠 Orange bars: Medium frequency
   - Moderate importance
   
🟢 Green bars: Rare words (high IDF)
   - Appear in few documents
   - Most distinctive/important

Why this matters:
✓ Common words like "the", "a" get low weights
✓ Distinctive words like "cat", "dog" get high weights
✓ This makes TF-IDF good for search & classification
    """
    
    ax2.text(0.05, 0.95, explanation, fontsize=11, verticalalignment='top',
            family='monospace', bbox=dict(boxstyle='round', facecolor='#E6F3FF', alpha=0.9, pad=1),
            transform=ax2.transAxes)
    
    plt.tight_layout()
    plt.savefig('02_idf_distribution.png', dpi=150, bbox_inches='tight')
    print("[OK] Saved: 02_idf_distribution.png")
    plt.close()


def visualize_tfidf_similarities():
    """Visualize document similarities using TF-IDF."""
    # Create sample documents
    documents = [
        ["python", "is", "a", "programming", "language"],
        ["java", "is", "also", "a", "programming", "language"],
        ["machine", "learning", "is", "powerful", "for", "ai"],
    ]
    
    # Train TF-IDF
    tfidf = TFIDF()
    tfidf.fit(documents)
    
    # Compute pairwise document similarities
    doc_vectors = [tfidf.transform(doc) for doc in documents]
    similarity_matrix = np.zeros((len(documents), len(documents)))
    
    for i in range(len(documents)):
        for j in range(len(documents)):
            similarity_matrix[i, j] = tfidf.cosine_similarity(doc_vectors[i], doc_vectors[j])
    
    # Create visualization
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Heatmap
    im = ax.imshow(similarity_matrix, cmap='RdYlGn', vmin=0, vmax=1, aspect='auto')
    
    # Labels
    doc_labels = ['Doc 1\n(Python)', 'Doc 2\n(Java)', 'Doc 3\n(ML/AI)']
    ax.set_xticks(range(3))
    ax.set_yticks(range(3))
    ax.set_xticklabels(doc_labels)
    ax.set_yticklabels(doc_labels)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Cosine Similarity', rotation=270, labelpad=20)
    
    # Add text annotations
    for i in range(3):
        for j in range(3):
            text = ax.text(j, i, f'{similarity_matrix[i, j]:.3f}',
                          ha="center", va="center", color="black", fontsize=14, fontweight='bold')
    
    ax.set_title('Document Similarity Matrix\nUsing TF-IDF Cosine Distance', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Add interpretation
    fig.text(0.5, 0.02, 'Doc 1 & 2 are most similar (both about programming languages) | Doc 3 is different (AI focus)',
            ha='center', fontsize=11, style='italic', bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.1)
    plt.savefig('03_tfidf_similarities.png', dpi=150, bbox_inches='tight')
    print("[OK] Saved: 03_tfidf_similarities.png")
    plt.close()


def visualize_sgns_vs_tfidf_comparison():
    """Side-by-side comparison of SGNS and TF-IDF approaches."""
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.3)
    
    # Title
    fig.suptitle('Skip-gram with Negative Sampling vs TF-IDF: Complete Comparison', 
                fontsize=16, fontweight='bold', y=0.98)
    
    # ===== ROW 1: What they learn =====
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.axis('off')
    ax1.text(0.5, 0.9, 'SGNS: What It Learns', ha='center', fontsize=13, fontweight='bold',
            transform=ax1.transAxes)
    sgns_text = """
✓ Semantic relationships
✓ Word context patterns
✓ Analogies (king - man + woman = queen)
✓ Dense embeddings (50-300 dimensions)
✓ Captures meaning from context
    """
    ax1.text(0.05, 0.7, sgns_text, fontsize=10, verticalalignment='top',
            transform=ax1.transAxes, family='monospace',
            bbox=dict(boxstyle='round', facecolor='#FFE6E6', alpha=0.9, pad=1))
    
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.axis('off')
    ax2.text(0.5, 0.9, 'TF-IDF: What It Learns', ha='center', fontsize=13, fontweight='bold',
            transform=ax2.transAxes)
    tfidf_text = """
✓ Statistical importance
✓ Word rarity in corpus
✓ Document-word relationships
✓ Sparse vectors (one per word)
✓ Measures: "How important is this word?"
    """
    ax2.text(0.05, 0.7, tfidf_text, fontsize=10, verticalalignment='top',
            transform=ax2.transAxes, family='monospace',
            bbox=dict(boxstyle='round', facecolor='#E6F3FF', alpha=0.9, pad=1))
    
    # ===== ROW 2: Key characteristics =====
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.axis('off')
    ax3.text(0.5, 0.9, 'SGNS: Characteristics', ha='center', fontsize=13, fontweight='bold',
            transform=ax3.transAxes)
    sgns_char = """
Speed:        Moderate (needs training)
Training:     Gradient descent over epochs
Input:        Text corpus
Interpretability: Low (black box embeddings)
Modern:       Very (foundation of transformers)
Use case:     Semantic search, NLP tasks
    """
    ax3.text(0.05, 0.7, sgns_char, fontsize=10, verticalalignment='top',
            transform=ax3.transAxes, family='monospace',
            bbox=dict(boxstyle='round', facecolor='#FFE6E6', alpha=0.9, pad=1))
    
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    ax4.text(0.5, 0.9, 'TF-IDF: Characteristics', ha='center', fontsize=13, fontweight='bold',
            transform=ax4.transAxes)
    tfidf_char = """
Speed:        Very fast (formula-based)
Training:     Simple formula (no gradient descent)
Input:        Document collection
Interpretability: High (simple formulas)
Modern:       Classic (still useful baseline)
Use case:     Information retrieval, document search
    """
    ax4.text(0.05, 0.7, tfidf_char, fontsize=10, verticalalignment='top',
            transform=ax4.transAxes, family='monospace',
            bbox=dict(boxstyle='round', facecolor='#E6F3FF', alpha=0.9, pad=1))
    
    # ===== ROW 3: When to use each =====
    ax5 = fig.add_subplot(gs[2, :])
    ax5.axis('off')
    ax5.text(0.5, 0.95, 'When to Use Each Method', ha='center', fontsize=13, fontweight='bold',
            transform=ax5.transAxes)
    
    comparison = """
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ Use SGNS when:                                  │ Use TF-IDF when:                          │
├─────────────────────────────────────────────────┼──────────────────────────────────────────┤
│ • You need semantic understanding               │ • You need fast, interpretable results   │
│ • Building NLP models (translation, Q&A)        │ • Searching/indexing documents           │
│ • You have lots of unlabeled text               │ • You need to explain word importance    │
│ • Training time is available                    │ • Working with bag-of-words paradigm     │
│ • You want to capture analogies                 │ • Document classification is the goal    │
│ • Building modern transformers                  │ • Baseline comparison is needed          │
└─────────────────────────────────────────────────┴──────────────────────────────────────────┘
    """
    ax5.text(0.05, 0.75, comparison, fontsize=9, verticalalignment='top',
            transform=ax5.transAxes, family='monospace',
            bbox=dict(boxstyle='round', facecolor='#FFFFCC', alpha=0.9, pad=1))
    
    plt.savefig('04_sgns_vs_tfidf_comparison.png', dpi=150, bbox_inches='tight')
    print("[OK] Saved: 04_sgns_vs_tfidf_comparison.png")
    plt.close()


def main():
    print("\n" + "="*70)
    print("Skip-gram with Negative Sampling & TF-IDF - Visualization Generator")
    print("="*70)
    print("\nGenerating visualizations for classroom teaching...\n")
    
    print("TF-IDF Visualizations (teach these first - they're simpler):")
    visualize_tfidf_matrix()
    visualize_idf_distribution()
    visualize_tfidf_similarities()
    visualize_sgns_vs_tfidf_comparison()
    
    print("\nSGNS Visualizations (teach these after TF-IDF):")
    visualize_context_window()
    visualize_sampling_process()
    model = visualize_word_embeddings()
    visualize_similarity_heatmap(model)
    visualize_algorithm_steps()
    visualize_training_dynamics()
    create_infographic()
    
    print("\n" + "="*70)
    print("All visualizations generated successfully!")
    print("="*70)
    print("\nGenerated files (in teaching order):")
    print("\n  TF-IDF VISUALIZATIONS (teach first - simpler, interpretable):")
    print("  01_tfidf_matrix.png           - Document-term matrix heatmap")
    print("  02_idf_distribution.png       - Word importance distribution")
    print("  03_tfidf_similarities.png     - Document similarity comparison")
    print("  04_sgns_vs_tfidf_comparison.png - Side-by-side method comparison")
    print("\n  SKIP-GRAM VISUALIZATIONS (teach after TF-IDF - more complex):")
    print("  05_context_window.png         - How the context window slides over text")
    print("  06_sampling_process.png       - Positive vs negative sampling visualization")
    print("  07_embeddings_2d.png          - Word embeddings space (t-SNE projection)")
    print("  08_similarity_heatmap.png     - Similarity matrix between words")
    print("  09_algorithm_steps.png        - Step-by-step algorithm flow")
    print("  10_training_dynamics.png      - How embeddings evolve during training")
    print("  11_infographic_sgns.png       - SGNS summary infographic")
    print("\n[OK] Ready for classroom presentation!\n")


if __name__ == "__main__":
    main()
