"""
Skip-gram with Negative Sampling (SGNS) Implementation

Skip-gram is a word embedding model that learns to represent words as dense vectors.
The key idea: words that appear in similar contexts should have similar vector representations.

Algorithm Overview:
1. For each word in a sentence, predict its context words (nearby words)
2. Use negative sampling to make training efficient (avoid computing softmax over entire vocabulary)
3. Negative sampling: for each true context word, sample k random "negative" words
   - Maximize dot product between target word and true context words
   - Minimize dot product between target word and negative words
"""

import numpy as np
from collections import defaultdict
import math


class SkipGramNegativeSampling:
    """
    Skip-gram with Negative Sampling word embedding model.
    
    Attributes:
        embedding_dim: Dimension of word vectors
        learning_rate: Learning rate for gradient updates
        negative_samples: Number of negative samples per positive sample
        window_size: Context window size on each side of target word
    """
    
    def __init__(self, embedding_dim=100, learning_rate=0.025, negative_samples=5, window_size=2):
        self.embedding_dim = embedding_dim
        self.learning_rate = learning_rate
        self.negative_samples = negative_samples
        self.window_size = window_size
        
        self.vocab = {}  # word -> index mapping
        self.word_vectors = None  # Target word embeddings (V x D)
        self.context_vectors = None  # Context word embeddings (V x D)
        self.word_freq = defaultdict(int)  # Word frequency counts
        
    def build_vocab(self, sentences):
        """Build vocabulary from sentences."""
        print("[1/4] Building vocabulary...")
        for sentence in sentences:
            for word in sentence:
                self.word_freq[word] += 1
        
        # Create word-to-index mapping
        for idx, word in enumerate(sorted(self.word_freq.keys())):
            self.vocab[word] = idx
        
        vocab_size = len(self.vocab)
        print(f"  Vocabulary size: {vocab_size}")
        
        # Initialize embedding matrices with small random values
        self.word_vectors = np.random.normal(0, 0.01, (vocab_size, self.embedding_dim))
        self.context_vectors = np.random.normal(0, 0.01, (vocab_size, self.embedding_dim))
        
    def _get_negative_samples(self, context_word_idx, num_samples):
        """
        Sample negative words according to word frequency.
        Higher frequency words are more likely to be sampled.
        Uses unigram distribution raised to 3/4 power (empirically better).
        """
        vocab_size = len(self.vocab)
        
        # Adjust num_samples if vocab is very small (allow replacement in that case)
        actual_samples = min(num_samples, vocab_size - 1)
        use_replacement = vocab_size <= num_samples
        
        # Create sampling probabilities: word_freq^0.75
        freq_weights = np.array([self.word_freq[word] ** 0.75 for word in sorted(self.word_freq.keys())])
        probabilities = freq_weights / freq_weights.sum()
        
        # Sample negative indices
        negative_indices = np.random.choice(
            vocab_size, 
            size=actual_samples, 
            p=probabilities,
            replace=use_replacement
        )
        
        # Ensure context word is not in negatives
        negative_indices = negative_indices[negative_indices != context_word_idx]
        
        return negative_indices[:num_samples]
    
    def _sigmoid(self, x):
        """Sigmoid activation: 1 / (1 + e^-x). Maps to (0, 1)."""
        return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))
    
    def _train_pair(self, target_idx, context_idx):
        """
        Train one (target, context) word pair using negative sampling.
        
        Objective:
        - Maximize: log(sigmoid(v_context · v_target))
        - Minimize: sum(log(sigmoid(-v_neg · v_target))) for negative samples
        """
        # Get target word vector
        target_vec = self.word_vectors[target_idx]  # (D,)
        
        # ===== POSITIVE SAMPLE (true context word) =====
        # We want to maximize dot product: v_context · v_target
        context_vec = self.context_vectors[context_idx]  # (D,)
        dot_product = np.dot(context_vec, target_vec)  # scalar
        
        # Sigmoid(dot_product) should be close to 1
        pred = self._sigmoid(dot_product)  # (0, 1)
        error = 1.0 - pred  # error = (1 - pred)
        
        # Gradient of sigmoid: sigma(x) * (1 - sigma(x))
        # Update: move vectors closer if error is high
        self.context_vectors[context_idx] += self.learning_rate * error * target_vec
        self.word_vectors[target_idx] += self.learning_rate * error * context_vec
        
        # ===== NEGATIVE SAMPLES =====
        # We want to minimize dot product: v_neg · v_target (make it negative)
        negative_indices = self._get_negative_samples(context_idx, self.negative_samples)
        
        for neg_idx in negative_indices:
            neg_vec = self.context_vectors[neg_idx]
            dot_product = np.dot(neg_vec, target_vec)
            
            # Sigmoid(dot_product) should be close to 0
            pred = self._sigmoid(dot_product)  # (0, 1)
            error = 0.0 - pred  # error = (0 - pred) = -pred
            
            # Update: move vectors apart
            self.context_vectors[neg_idx] += self.learning_rate * error * target_vec
            self.word_vectors[target_idx] += self.learning_rate * error * neg_vec
    
    def train(self, sentences, epochs=5):
        """
        Train the Skip-gram model on sentences.
        
        For each sentence:
        - Slide context window over words
        - For each target word, predict context words
        - Use negative sampling to make training efficient
        """
        print(f"[2/4] Training for {epochs} epochs...")
        
        total_pairs = 0
        for epoch in range(epochs):
            epoch_loss = 0
            pair_count = 0
            
            for sentence in sentences:
                for target_pos, target_word in enumerate(sentence):
                    # Get context words within window
                    context_start = max(0, target_pos - self.window_size)
                    context_end = min(len(sentence), target_pos + self.window_size + 1)
                    
                    target_idx = self.vocab[target_word]
                    
                    for context_pos in range(context_start, context_end):
                        if context_pos == target_pos:
                            continue  # Skip the target word itself
                        
                        context_word = sentence[context_pos]
                        context_idx = self.vocab[context_word]
                        
                        self._train_pair(target_idx, context_idx)
                        pair_count += 1
            
            total_pairs = max(total_pairs, pair_count)
            print(f"  Epoch {epoch + 1}/{epochs}: trained on {pair_count} word pairs")
        
        print(f"  Total training pairs processed: {total_pairs}")
    
    def get_vector(self, word):
        """Get embedding vector for a word."""
        if word not in self.vocab:
            raise ValueError(f"Word '{word}' not in vocabulary")
        idx = self.vocab[word]
        return self.word_vectors[idx]
    
    def most_similar(self, word, topn=5):
        """Find most similar words using cosine similarity."""
        if word not in self.vocab:
            return []
        
        word_vec = self.get_vector(word)
        word_vec_norm = word_vec / (np.linalg.norm(word_vec) + 1e-10)
        
        # Compute cosine similarity with all words
        vocab_vecs_norm = self.word_vectors / (np.linalg.norm(self.word_vectors, axis=1, keepdims=True) + 1e-10)
        similarities = np.dot(vocab_vecs_norm, word_vec_norm)
        
        # Get top similar words (excluding the word itself)
        top_indices = np.argsort(-similarities)
        results = []
        for idx in top_indices:
            if similarities[idx] < 0.99:  # Exclude the word itself
                word_found = [w for w, i in self.vocab.items() if i == idx][0]
                results.append((word_found, similarities[idx]))
                if len(results) == topn:
                    break
        
        return results


def main_menu():
    """Display main menu for choosing demonstration."""
    print("\n" + "=" * 70)
    print("NLP Word Representation Methods - Demonstration")
    print("=" * 70)
    print("\nChoose what to demonstrate:")
    print("\n  1. Skip-gram with Negative Sampling (SGNS)")
    print("     -> Semantic embeddings, contextual, slower, better analogies")
    print("     -> Output: Dense word vectors learned from context")
    print("\n  2. TF-IDF (Term Frequency - Inverse Document Frequency)")
    print("     -> Statistical importance, fast, interpretable")
    print("     -> Output: Word importance weights in documents")
    print("\n  3. SGNS vs TF-IDF Comparison")
    print("     -> Side-by-side comparison of both approaches")
    print("     -> Shows when to use each method")
    print("\n  4. Run Both (SGNS -> TF-IDF -> Comparison)")
    print("     -> Complete tour of all techniques")
    print("\n  0. Exit")
    print("\n" + "=" * 70)
    
    while True:
        choice = input("\nSelect option (0-4): ").strip()
        if choice in ['0', '1', '2', '3', '4']:
            return choice
        print("Invalid choice. Please select 0-4.")


def demo_sgns():
    """Demonstrate Skip-gram with Negative Sampling on a toy corpus."""
    
    # Simple toy corpus
    sentences = [
        ["king", "is", "a", "man"],
        ["queen", "is", "a", "woman"],
        ["prince", "is", "a", "boy"],
        ["princess", "is", "a", "girl"],
        ["king", "and", "queen", "rule", "the", "kingdom"],
        ["man", "and", "woman", "walked", "in", "the", "park"],
    ]
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION 1: Skip-gram with Negative Sampling (SGNS)")
    print("=" * 70)
    print()
    
    # Initialize model
    print("[0/4] Initializing model...")
    model = SkipGramNegativeSampling(
        embedding_dim=50,
        learning_rate=0.025,
        negative_samples=5,
        window_size=2
    )
    print(f"  Embedding dimension: 50")
    print(f"  Negative samples per pair: 5")
    print(f"  Context window size: 2")
    print()
    
    # Build vocabulary
    model.build_vocab(sentences)
    print()
    
    # Train model
    model.train(sentences, epochs=10)
    print()
    
    # Evaluate: find similar words
    print("[3/4] Finding similar words...")
    test_words = ["king", "queen", "man", "woman"]
    for word in test_words:
        if word in model.vocab:
            similar = model.most_similar(word, topn=3)
            print(f"  {word:10s} -> {similar}")
    print()
    
    # Get word vectors
    print("[4/4] Word vectors (first 3 dimensions shown):")
    for word in test_words:
        vec = model.get_vector(word)
        print(f"  {word:10s}: {vec[:3]}")
    print()
    
    print("=" * 60)
    print("Key Insights:")
    print("=" * 60)
    print("""
1. NEGATIVE SAMPLING makes training efficient:
   - Instead of computing softmax over 10K+ words, we only compute loss for 1 positive + k negatives
   - This reduces computational cost from O(V) to O(k) per training step

2. CONTEXT WINDOW captures word relationships:
   - Words appearing nearby in text should have similar meanings
   - "king" and "queen" appear in similar contexts ("is", "a", "rule", "the")

3. WORD FREQUENCY WEIGHTING improves sampling:
   - Negative samples are drawn from P(w) proportional to freq(w)^0.75
   - Slightly favors common words, prevents rare words from dominating negatives

4. TWO EMBEDDING MATRICES (pragmatic design choice):
   - word_vectors: used as target words
   - context_vectors: used as context predictions
   - Often only word_vectors are used in downstream tasks (could share weights)
    """)
    
    # Show comparison with TF-IDF
    compare_sgns_vs_tfidf()


def demo_tfidf():
    """Demonstrate TF-IDF on a toy corpus."""
    
    documents = [
        ["the", "cat", "sat", "on", "the", "mat"],
        ["a", "dog", "sat", "on", "the", "floor"],
        ["the", "cat", "and", "dog", "play", "together"],
    ]
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION 2: TF-IDF (Term Frequency - Inverse Document Frequency)")
    print("=" * 70)
    print()
    
    print("[What is TF-IDF?]")
    print("  TF (Term Frequency): How often a word appears in a document")
    print("  IDF (Inverse Document Frequency): How unique the word is across documents")
    print("  TF-IDF = TF × IDF: Measures word importance to a specific document")
    print()
    
    print("[Corpus]")
    for i, doc in enumerate(documents, 1):
        print(f"  Doc {i}: {' '.join(doc)}")
    print()
    
    # Train TF-IDF
    print("[Training TF-IDF]")
    tfidf = TFIDF()
    tfidf.fit(documents)
    print(f"  Vocabulary size: {len(tfidf.vocab)}")
    print()
    
    # Transform documents
    print("[TF-IDF Vectors (top 3 words per document)]")
    doc_vectors = []
    for i, doc in enumerate(documents, 1):
        vec = tfidf.transform(doc)
        doc_vectors.append(vec)
        
        top_indices = np.argsort(-vec)[:3]
        top_words = [(list(tfidf.vocab.keys())[idx], f"{vec[idx]:.3f}") 
                     for idx in top_indices if vec[idx] > 0]
        print(f"  Doc {i}: {top_words}")
    print()
    
    # Document similarities
    print("[Document Similarities]")
    for i in range(len(documents)):
        for j in range(i+1, len(documents)):
            sim = tfidf.cosine_similarity(doc_vectors[i], doc_vectors[j])
            print(f"  Doc {i+1} vs Doc {j+1}: {sim:.3f}")
    print()
    
    print("[Key Insights]")
    print("  1. 'the' has low importance (very common, high frequency everywhere)")
    print("  2. 'cat' and 'dog' have high importance (appear in few documents, unique)")
    print("  3. TF-IDF is FAST - just formula-based, no training loops")
    print("  4. TF-IDF is INTERPRETABLE - can explain why words matter")
    print("  5. Perfect for: Document search, information retrieval, text classification")
    print()


def demo_comparison():
    """Compare SGNS and TF-IDF directly."""
    print("\n" + "=" * 70)
    print("DEMONSTRATION 3: SGNS vs TF-IDF - Detailed Comparison")
    print("=" * 70)
    print()
    
    corpus = [
        ["machine", "learning", "is", "powerful"],
        ["deep", "learning", "uses", "neural", "networks"],
        ["machine", "learning", "and", "deep", "learning", "are", "related"],
    ]
    
    print("[Test Corpus]")
    for i, sent in enumerate(corpus, 1):
        print(f"  {i}. {' '.join(sent)}")
    print()
    
    # TF-IDF approach
    print("-" * 70)
    print("APPROACH 1: TF-IDF")
    print("-" * 70)
    
    tfidf = TFIDF()
    tfidf.fit(corpus)
    
    print("\nWhat TF-IDF learns:")
    print("  • Word importance based on rarity")
    print("  • 'learning' appears 3x (common, low IDF)")
    print("  • 'neural' appears 1x (rare, high IDF)")
    print("  • Formula: TF × IDF = (freq/total) × log(docs/docs_with_word)")
    
    test_doc = ["machine", "learning", "neural"]
    vec = tfidf.transform(test_doc)
    print(f"\nTF-IDF for: {test_doc}")
    top_idx = np.argsort(-vec)[:3]
    for idx in top_idx:
        if vec[idx] > 0:
            word = list(tfidf.vocab.keys())[idx]
            print(f"  {word}: {vec[idx]:.3f}")
    
    print("\nAdvantages:")
    print("  ✓ Very fast (no training needed)")
    print("  ✓ Interpretable (know why each word matters)")
    print("  ✓ Works with any corpus size")
    print("  ✓ Great for document search")
    
    # SGNS approach
    print("\n" + "-" * 70)
    print("APPROACH 2: SGNS")
    print("-" * 70)
    
    model = SkipGramNegativeSampling(embedding_dim=25, learning_rate=0.025)
    model.build_vocab(corpus)
    model.train(corpus, epochs=10)
    
    print("\nWhat SGNS learns:")
    print("  • Semantic relationships from context")
    print("  • 'machine' and 'deep' are similar (both modify 'learning')")
    print("  • 'neural' is similar to 'networks' (appear together)")
    print("  • Learned through gradient descent on context prediction task")
    
    print("\nSimilar words (semantic):")
    for word in ["machine", "learning", "neural"]:
        if word in model.vocab:
            similar = model.most_similar(word, topn=2)
            print(f"  {word:10s}: {similar}")
    
    print("\nAdvantages:")
    print("  ✓ Captures semantic meaning")
    print("  ✓ Can find synonyms and analogies")
    print("  ✓ Transfer learning (use embeddings in other tasks)")
    print("  ✓ Dense vectors (all dimensions are meaningful)")
    
    # Comparison table
    print("\n" + "-" * 70)
    print("SIDE-BY-SIDE COMPARISON")
    print("-" * 70)
    print(f"\n{'Aspect':<25} {'TF-IDF':<30} {'SGNS':<30}")
    print("-" * 85)
    print(f"{'What it learns':<25} {'Word importance':<30} {'Word meanings':<30}")
    print(f"{'Training method':<25} {'Formula-based':<30} {'Gradient descent':<30}")
    print(f"{'Speed':<25} {'Instant':<30} {'Requires epochs':<30}")
    print(f"{'Interpretability':<25} {'High':<30} {'Low':<30}")
    print(f"{'Vector type':<25} {'Sparse (many 0s)':<30} {'Dense (no 0s)':<30}")
    print(f"{'Best for':<25} {'Search, retrieval':<30} {'Analogies, transfer':<30}")
    print(f"{'Computational cost':<25} {'O(vocab_size)':<30} {'O(epochs × corpus)':<30}")
    print("-" * 85)
    
    print("\n[Decision Guide]")
    print("  Choose TF-IDF if:")
    print("    • You need SPEED (instant results)")
    print("    • You need INTERPRETABILITY (know why results happen)")
    print("    • Working with document search or classification")
    print("    • Have limited computational resources")
    print()
    print("  Choose SGNS if:")
    print("    • You need SEMANTIC understanding")
    print("    • Want to find synonyms and analogies")
    print("    • Planning to use embeddings for transfer learning")
    print("    • Have time for training and GPU available")
    print()


def main():
    """Main entry point with menu system."""
    
    choice = main_menu()
    
    if choice == '0':
        print("\nGoodbye!")
        return
    elif choice == '1':
        demo_sgns()
    elif choice == '2':
        demo_tfidf()
    elif choice == '3':
        demo_comparison()
    elif choice == '4':
        demo_sgns()
        input("\n[Press Enter to continue to TF-IDF demonstration...]")
        demo_tfidf()
        input("\n[Press Enter to continue to comparison...]")
        demo_comparison()
    
    print("\n" + "=" * 70)
    print("Demonstration Complete!")
    print("=" * 70)
    print("\n✓ Ready for classroom use!")
    print("  Try different demonstrations to understand both approaches.")
    print()


class TFIDF:
    """
    TF-IDF (Term Frequency - Inverse Document Frequency) vectorizer.
    
    A faster, statistical alternative to SGNS:
    - TF: How often a word appears in a document
    - IDF: How unique the word is across all documents
    - TF-IDF: Measures how important a word is to a specific document
    
    Unlike SGNS (semantic), TF-IDF is statistical and interpretable.
    """
    
    def __init__(self):
        self.vocab = {}
        self.idf = {}
        self.documents = []
        
    def fit(self, documents):
        """
        Build vocabulary and compute IDF values.
        
        Args:
            documents: List of tokenized documents (each a list of words)
        """
        self.documents = documents
        
        # Build vocabulary
        word_count = defaultdict(int)
        doc_count = defaultdict(int)
        
        for doc in documents:
            doc_words = set(doc)
            for word in doc:
                word_count[word] += 1
            for word in doc_words:
                doc_count[word] += 1
        
        # Create word-to-index mapping
        for idx, word in enumerate(sorted(word_count.keys())):
            self.vocab[word] = idx
        
        # Compute IDF: log(total_docs / docs_containing_word)
        total_docs = len(documents)
        for word in self.vocab:
            self.idf[word] = np.log(total_docs / (doc_count[word] + 1e-10))
    
    def transform(self, document):
        """
        Transform a document into TF-IDF vector.
        
        Args:
            document: List of words in document
            
        Returns:
            TF-IDF vector (sparse representation shown as dict)
        """
        vocab_size = len(self.vocab)
        tfidf_vector = np.zeros(vocab_size)
        
        # Compute term frequencies
        word_freq = defaultdict(int)
        for word in document:
            word_freq[word] += 1
        
        total_words = len(document)
        
        # Compute TF-IDF for each word
        for word, freq in word_freq.items():
            if word in self.vocab:
                idx = self.vocab[word]
                tf = freq / total_words
                idf = self.idf.get(word, 0)
                tfidf_vector[idx] = tf * idf
        
        return tfidf_vector
    
    def cosine_similarity(self, vec1, vec2):
        """Compute cosine similarity between two vectors."""
        norm1 = np.linalg.norm(vec1) + 1e-10
        norm2 = np.linalg.norm(vec2) + 1e-10
        return np.dot(vec1, vec2) / (norm1 * norm2)


def compare_sgns_vs_tfidf():
    """Demonstrate difference between SGNS and TF-IDF."""
    print("\n" + "="*60)
    print("SGNS vs TF-IDF: Conceptual Comparison")
    print("="*60)
    
    # Simple corpus
    documents = [
        ["the", "cat", "sat", "on", "the", "mat"],
        ["a", "dog", "sat", "on", "the", "floor"],
        ["the", "cat", "and", "dog", "play", "together"],
    ]
    
    print("\nCorpus (3 documents):")
    for i, doc in enumerate(documents, 1):
        print(f"  Doc {i}: {' '.join(doc)}")
    
    # TF-IDF approach
    print("\n[TF-IDF Approach]")
    tfidf = TFIDF()
    tfidf.fit(documents)
    
    # Transform documents
    print("\nTF-IDF vectors (showing top 3 words):")
    for i, doc in enumerate(documents, 1):
        vec = tfidf.transform(doc)
        top_indices = np.argsort(-vec)[:3]
        top_words = [(list(tfidf.vocab.keys())[idx], vec[idx]) for idx in top_indices if vec[idx] > 0]
        print(f"  Doc {i}: {top_words}")
    
    # Compare similarity using TF-IDF
    doc1_vec = tfidf.transform(documents[0])
    doc2_vec = tfidf.transform(documents[1])
    doc3_vec = tfidf.transform(documents[2])
    
    sim_12 = tfidf.cosine_similarity(doc1_vec, doc2_vec)
    sim_13 = tfidf.cosine_similarity(doc1_vec, doc3_vec)
    
    print(f"\nTF-IDF Document Similarities:")
    print(f"  Doc1 vs Doc2: {sim_12:.3f} (both have 'sat', 'on')")
    print(f"  Doc1 vs Doc3: {sim_13:.3f} (both have 'cat', 'dog')")
    
    # SGNS approach
    print("\n[SGNS Approach]")
    model = SkipGramNegativeSampling(embedding_dim=30, learning_rate=0.025)
    model.build_vocab(documents)
    model.train(documents, epochs=5)
    
    # Show similar words (semantic)
    print("\nSGNS: Similar words (semantic meaning):")
    for word in ["cat", "dog", "sat"]:
        if word in model.vocab:
            similar = model.most_similar(word, topn=2)
            print(f"  {word:6s}: {similar}")
    
    print("\n[Key Difference]")
    print("  TF-IDF:   'cat' and 'dog' have high weight (rare, important)")
    print("  SGNS:     'cat' and 'dog' are similar (appear in similar context)")
    print("\n  TF-IDF: Statistical (bag-of-words, fast, interpretable)")
    print("  SGNS:   Semantic (contextual, slower, better for analogies)")
    print("="*60)


