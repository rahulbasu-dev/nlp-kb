"""
Interactive Classroom Examples - Skip-gram with Negative Sampling

This script provides interactive examples and experiments for classroom teaching.
Run individual functions to demonstrate different concepts.
"""

import numpy as np
from sgns import SkipGramNegativeSampling, TFIDF
import matplotlib.pyplot as plt


def example_1_basic_usage():
    """
    Example 1: Basic Usage
    =====================
    Train a basic model and find similar words
    """
    try:
        output = []
        output.append("\n" + "="*70)
        output.append("EXAMPLE 1: Basic Usage - Train Model and Find Similar Words")
        output.append("="*70)
        
        # Simple corpus
        sentences = [
            ["the", "cat", "sat", "on", "the", "mat"],
            ["a", "dog", "sat", "on", "the", "floor"],
            ["the", "cat", "and", "dog", "are", "friends"],
        ]
        
        output.append("\nCorpus:")
        for i, s in enumerate(sentences, 1):
            output.append(f"  {i}. {' '.join(s)}")
        
        # Train
        output.append("\nTraining model...")
        model = SkipGramNegativeSampling(embedding_dim=30, learning_rate=0.02)
        model.build_vocab(sentences)
        model.train(sentences, epochs=5)
        
        # Find similarities
        output.append("\nWord Similarities:")
        test_words = ["cat", "dog", "sat", "the"]
        for word in test_words:
            similar = model.most_similar(word, topn=2)
            output.append(f"  {word:6s} -> {similar}")
        
        # Print all at once
        print("\n".join(output))
    except Exception as e:
        import traceback
        print("ERROR in example 1:")
        print(traceback.format_exc())


def example_2_hyperparameter_impact():
    """
    Example 2: Impact of Hyperparameters
    ====================================
    Show how different parameters affect learning
    """
    try:
        print("\n" + "="*70)
        print("EXAMPLE 2: Impact of Hyperparameters")
        print("="*70)
        
        sentences = [
            ["king", "is", "a", "powerful", "man"],
            ["queen", "is", "a", "powerful", "woman"],
            ["prince", "will", "become", "a", "king"],
            ["princess", "will", "become", "a", "queen"],
        ]
        
        configs = [
            {"name": "Small embeddings", "embedding_dim": 10},
            {"name": "Medium embeddings", "embedding_dim": 50},
            {"name": "Large embeddings", "embedding_dim": 100},
        ]
        
        for config in configs:
            model = SkipGramNegativeSampling(
                embedding_dim=config["embedding_dim"],
                learning_rate=0.025
            )
            model.build_vocab(sentences)
            model.train(sentences, epochs=10)
            
            print(f"\n{config['name']} (dim={config['embedding_dim']}):")
            similar_king = model.most_similar("king", topn=2)
            similar_queen = model.most_similar("queen", topn=2)
            print(f"  Similar to 'king':   {similar_king}")
            print(f"  Similar to 'queen':  {similar_queen}")
    except Exception as e:
        import traceback
        print("ERROR in example 2:")
        print(traceback.format_exc())


def example_3_context_window_effect():
    """
    Example 3: Effect of Context Window Size
    ========================================
    Show how larger windows capture more context
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Effect of Context Window Size")
    print("="*70)
    
    sentences = [
        ["the", "quick", "brown", "fox", "jumped", "over", "the", "lazy", "dog"],
    ]
    
    window_sizes = [1, 2, 5]
    
    print(f"\nSentence: {' '.join(sentences[0])}")
    print("Target word: 'jumped'")
    
    for window_size in window_sizes:
        model = SkipGramNegativeSampling(
            embedding_dim=20,
            window_size=window_size,
            learning_rate=0.025
        )
        model.build_vocab(sentences)
        model.train(sentences, epochs=10)
        
        similar = model.most_similar("jumped", topn=3)
        print(f"\nWindow size = {window_size}:")
        print(f"  Context: {similar}")
        print(f"  Insight: Larger windows learn from more distant words")


def example_4_corpus_effect():
    """
    Example 4: How Corpus Domain Affects Embeddings
    ================================================
    Show that word meanings are learned from corpus
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Corpus Domain Affects Learned Meanings")
    print("="*70)
    
    # Corpus 1: Sports domain
    sports_corpus = [
        ["the", "player", "scored", "a", "goal"],
        ["the", "goalkeeper", "made", "a", "save"],
        ["the", "referee", "made", "a", "call"],
        ["the", "team", "won", "the", "match"],
    ]
    
    # Corpus 2: Music domain  
    music_corpus = [
        ["the", "player", "played", "a", "note"],
        ["the", "guitarist", "made", "a", "sound"],
        ["the", "conductor", "led", "the", "orchestra"],
        ["the", "band", "won", "the", "award"],
    ]
    
    print("\nCORPUS 1 (Sports):")
    model1 = SkipGramNegativeSampling(embedding_dim=30)
    model1.build_vocab(sports_corpus)
    model1.train(sports_corpus, epochs=10)
    similar_player = model1.most_similar("player", topn=3)
    print(f"  Similar to 'player': {similar_player}")
    print(f"  → In sports context, 'player' is similar to action verbs")
    
    print("\nCORPUS 2 (Music):")
    model2 = SkipGramNegativeSampling(embedding_dim=30)
    model2.build_vocab(music_corpus)
    model2.train(music_corpus, epochs=10)
    similar_player = model2.most_similar("player", topn=3)
    print(f"  Similar to 'player': {similar_player}")
    print(f"  → In music context, 'player' learns different associations")


def example_5_embedding_inspection():
    """
    Example 5: Inspect Actual Embeddings
    ===================================
    Look at the raw vectors learned
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Inspecting Learned Embeddings")
    print("="*70)
    
    sentences = [
        ["king", "rules", "the", "kingdom"],
        ["queen", "rules", "the", "kingdom"],
        ["prince", "will", "rule", "the", "kingdom"],
        ["man", "and", "woman", "live", "in", "harmony"],
    ]
    
    model = SkipGramNegativeSampling(embedding_dim=8)  # Small for readability
    model.build_vocab(sentences)
    model.train(sentences, epochs=10)
    
    print("\nWord Vectors (8 dimensions for visualization):")
    for word in ["king", "queen", "prince", "man", "woman"]:
        vec = model.get_vector(word)
        print(f"  {word:6s}: {vec}")
    
    print("\nObservations:")
    print("  1. Each word is a point in 8D space")
    print("  2. Similar words should have similar vectors")
    print("  3. Cosine distance measures similarity")
    
    # Show vector norms
    print("\nVector magnitudes (L2 norm):")
    for word in ["king", "queen", "prince", "man", "woman"]:
        vec = model.get_vector(word)
        norm = np.linalg.norm(vec)
        print(f"  {word:6s}: {norm:.4f}")


def example_6_math_behind_training():
    """
    Example 6: Math Behind Training
    ==============================
    Show the math of a single training update
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Math Behind Training (Simplified)")
    print("="*70)
    
    print("""
    For each (target, context_word) pair:
    
    1. POSITIVE SAMPLE (Context word):
       • Compute: dot = v_context · v_target
       • Prediction: pred = sigmoid(dot) ∈ [0, 1]
       • Target: we want pred ≈ 1 (high similarity)
       • Error: error = 1 - pred
       • Update: v_new = v_old + learning_rate * error * other_vector
    
    2. NEGATIVE SAMPLES (Random words):
       • Compute: dot = v_random · v_target
       • Prediction: pred = sigmoid(dot) ∈ [0, 1]
       • Target: we want pred ≈ 0 (low similarity)
       • Error: error = 0 - pred = -pred
       • Update: v_new = v_old + learning_rate * error * target_vector
    
    INTUITION:
    • If dot product is too high → error is negative → vectors move apart
    • If dot product is too low → error is positive → vectors move closer
    • This is contrastive learning: maximize signal, minimize noise
    """)
    
    print("\nNumerical Example:")
    print("  Target word: 'king' with vector [0.5, 0.3]")
    print("  Context word: 'queen' with vector [0.48, 0.32]")
    print("  Learning rate: 0.1")
    
    v_target = np.array([0.5, 0.3])
    v_context = np.array([0.48, 0.32])
    learning_rate = 0.1
    
    dot = np.dot(v_context, v_target)
    pred = 1.0 / (1.0 + np.exp(-dot))
    error = 1.0 - pred
    
    print(f"\n  Dot product: {dot:.4f}")
    print(f"  Sigmoid(dot): {pred:.4f} (we want 1.0)")
    print(f"  Error: {error:.4f}")
    
    v_context_new = v_context + learning_rate * error * v_target
    print(f"\n  v_context_old: {v_context}")
    print(f"  v_context_new: {v_context_new}")
    print(f"  Change: {v_context_new - v_context} (moved closer)")


def example_7_why_fast():
    """
    Example 7: Why Negative Sampling is Fast
    =======================================
    Compare cost of different approaches
    """
    print("\n" + "="*70)
    print("EXAMPLE 7: Why Negative Sampling is Fast")
    print("="*70)
    
    vocab_sizes = [1000, 10000, 100000, 1000000]
    k_negatives = 5
    
    print(f"\nComputing cost for one training step:")
    print(f"(Assuming one (target, context) pair)")
    print()
    print(f"{'Vocabulary Size':<20} {'Softmax Cost':<20} {'Neg Sampling Cost':<20} {'Speedup':<10}")
    print("-" * 70)
    
    for vocab_size in vocab_sizes:
        softmax_cost = vocab_size  # Need to compute for all words
        neg_sampling_cost = k_negatives  # Only compute for k samples
        speedup = softmax_cost / neg_sampling_cost
        
        print(f"{vocab_size:<20} {softmax_cost:<20} {neg_sampling_cost:<20} {speedup:.0f}x")
    
    print("\nCONCLUSION:")
    print("  Softmax scales with vocabulary size (O(V))")
    print("  Negative Sampling is constant (O(k), typically k=5-20)")
    print("  For 1M word vocabulary: 200,000x faster! ⚡")


def example_8_tfidf_basics():
    """
    Example 8: TF-IDF Basics
    =======================
    Understand TF-IDF as a faster alternative to SGNS
    """
    print("\n" + "="*70)
    print("EXAMPLE 8: TF-IDF Basics - Statistical Approach to Word Importance")
    print("="*70)
    
    documents = [
        ["machine", "learning", "is", "powerful"],
        ["deep", "learning", "uses", "neural", "networks"],
        ["machine", "learning", "and", "deep", "learning", "are", "related"],
    ]
    
    print("\nCorpus (3 documents):")
    for i, doc in enumerate(documents, 1):
        print(f"  Doc {i}: {' '.join(doc)}")
    
    # Train TF-IDF
    print("\nTraining TF-IDF model...")
    tfidf = TFIDF()
    tfidf.fit(documents)
    print(f"  Vocabulary size: {len(tfidf.vocab)}")
    
    # Show TF-IDF vectors
    print("\nTF-IDF vectors (top 3 words per document):")
    doc_vectors = []
    for i, doc in enumerate(documents, 1):
        vec = tfidf.transform(doc)
        doc_vectors.append(vec)
        
        # Get top words
        top_indices = np.argsort(-vec)[:3]
        top_words = [(list(tfidf.vocab.keys())[idx], f"{vec[idx]:.3f}") 
                     for idx in top_indices if vec[idx] > 0]
        print(f"  Doc {i}: {top_words}")
    
    # Show document similarity
    print("\nDocument Similarities (using TF-IDF cosine distance):")
    for i in range(len(documents)):
        for j in range(i+1, len(documents)):
            sim = tfidf.cosine_similarity(doc_vectors[i], doc_vectors[j])
            print(f"  Doc {i+1} vs Doc {j+1}: {sim:.3f}")
    
    print("\nKey Insights:")
    print("  1. Words appearing in fewer documents get higher IDF")
    print("  2. TF-IDF is FAST - just formula-based, no gradient descent")
    print("  3. TF-IDF is INTERPRETABLE - can explain why words are important")
    print("  4. TF-IDF works on bag-of-words (ignores word order)")


def example_9_sgns_vs_tfidf():
    """
    Example 9: SGNS vs TF-IDF Comparison
    ===================================
    Side-by-side comparison of the two approaches
    """
    print("\n" + "="*70)
    print("EXAMPLE 9: SGNS vs TF-IDF - Head-to-Head Comparison")
    print("="*70)
    
    corpus = [
        ["python", "is", "a", "programming", "language"],
        ["java", "is", "also", "a", "programming", "language"],
        ["python", "and", "java", "are", "popular"],
    ]
    
    print("\nCorpus:")
    for i, sent in enumerate(corpus, 1):
        print(f"  {i}. {' '.join(sent)}")
    
    print("\n" + "-"*70)
    print("APPROACH 1: TF-IDF (Statistical)")
    print("-"*70)
    
    tfidf = TFIDF()
    tfidf.fit(corpus)
    
    print("\nTF-IDF Perspective:")
    print("  'python' is important (appears in 2/3 docs)")
    print("  'is' is unimportant (appears in 2/3 docs, very common)")
    print("  'programming' is distinctive (rare and meaningful)")
    
    test_doc = ["python", "programming", "language"]
    vec = tfidf.transform(test_doc)
    print(f"\nTF-IDF for '{' '.join(test_doc)}':")
    top_idx = np.argsort(-vec)[:3]
    for idx in top_idx:
        if vec[idx] > 0:
            word = list(tfidf.vocab.keys())[idx]
            print(f"  {word}: {vec[idx]:.3f}")
    
    print("\n" + "-"*70)
    print("APPROACH 2: SGNS (Semantic)")
    print("-"*70)
    
    model = SkipGramNegativeSampling(embedding_dim=20, learning_rate=0.025)
    model.build_vocab(corpus)
    model.train(corpus, epochs=10)
    
    print("\nSGNS Perspective:")
    print("  'python' and 'java' are similar (similar context)")
    print("  'is' appears with many words (very central)")
    print("  'language' goes with 'programming' (contextual)")
    
    test_words = ["python", "java", "language"]
    print(f"\nSGNS Similarities:")
    for word in test_words:
        if word in model.vocab:
            similar = model.most_similar(word, topn=2)
            print(f"  {word:12s}: {similar}")
    
    print("\n" + "-"*70)
    print("COMPARISON SUMMARY")
    print("-"*70)
    print("\nTF-IDF: Statistical, Fast, Interpretable")
    print("  • Measures: Word rarity and importance")
    print("  • Speed: O(vocab_size) - very fast")
    print("  • Use case: Document search, information retrieval")
    print("  • Vector type: Sparse (most zeros)")
    
    print("\nSGNS: Semantic, Slower, Better analogies")
    print("  • Measures: Contextual word similarity")
    print("  • Speed: O(1) per step but needs many epochs")
    print("  • Use case: Word relationships, embeddings for other tasks")
    print("  • Vector type: Dense (no zeros)")
    
    print("\nWhen to use each:")
    print("  Use TF-IDF if: You need fast, simple, interpretable results")
    print("  Use SGNS if: You want semantic relationships and transfer learning")


def main():
    """Run all examples interactively"""
    examples = [
        ("1", "Basic Usage", example_1_basic_usage),
        ("2", "Hyperparameter Impact", example_2_hyperparameter_impact),
        ("3", "Context Window Effect", example_3_context_window_effect),
        ("4", "Corpus Domain Effect", example_4_corpus_effect),
        ("5", "Embedding Inspection", example_5_embedding_inspection),
        ("6", "Math Behind Training", example_6_math_behind_training),
        ("7", "Why Negative Sampling is Fast", example_7_why_fast),
        ("8", "TF-IDF Basics", example_8_tfidf_basics),
        ("9", "SGNS vs TF-IDF Comparison", example_9_sgns_vs_tfidf),
    ]
    
    print("\n" + "="*70)
    print("Skip-gram with Negative Sampling - Interactive Classroom Examples")
    print("="*70)
    print("\nAvailable examples:")
    for num, name, _ in examples:
        print(f"  {num}. {name}")
    print(f"  {'all':<3} Run all examples")
    print(f"  {'quit':<3} Exit")
    
    while True:
        choice = input("\nSelect example to run: ").strip().lower()
        
        if choice == "quit":
            print("Goodbye!")
            break
        elif choice == "all":
            for num, name, func in examples:
                func()
                input("\nPress Enter to continue to next example...")
        else:
            for num, name, func in examples:
                if num == choice:
                    func()
                    break
            else:
                if choice:
                    print(f"Unknown option: {choice}")


if __name__ == "__main__":
    main()
