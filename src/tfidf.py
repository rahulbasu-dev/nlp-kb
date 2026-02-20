import math
import re
from collections import Counter

class TFIDFVectorizer:
    def __init__(self, use_smoothing=False):
        self.vocabulary = []
        self.idf_values = {}
        self.tfidf_matrix = []
        self.use_smoothing = use_smoothing
        self.tokenized_docs = []
        self.tf_matrix = []

    def preprocess(self, text):
        return re.findall(r'[a-z]+', text.lower())

    def compute_tf(self, tokens):
        counts = Counter(tokens)
        total = len(tokens)
        if total == 0: return {}
        return {term: count/total for term, count in counts.items()}

    def compute_idf(self, tokenized_docs):
        N = len(tokenized_docs)
        doc_freq = Counter()
        for tokens in tokenized_docs:
            for term in set(tokens):
                doc_freq[term] += 1

        idf = {}
        for term in self.vocabulary:
            df = doc_freq.get(term, 0)
            if self.use_smoothing:
                idf[term] = math.log10(N / (1 + df))
            else:
                idf[term] = math.log10(N / df) if df > 0 else 0
        return idf

    def fit_transform(self, documents):
        self.tokenized_docs = [self.preprocess(doc) for doc in documents]
        self.vocabulary = sorted(set(t for tokens in self.tokenized_docs for t in tokens))
        self.tf_matrix = [self.compute_tf(tokens) for tokens in self.tokenized_docs]
        self.idf_values = self.compute_idf(self.tokenized_docs)

        self.tfidf_matrix = []
        for tf in self.tf_matrix:
            tfidf = {term: tf.get(term, 0) * self.idf_values.get(term, 0)
                     for term in self.vocabulary}
            self.tfidf_matrix.append(tfidf)
        return self.tfidf_matrix

def explain_interpretation():
    """Prints a human-readable guide on what the numbers mean."""
    print("\n" + "="*60)
    print("HOW TO INTERPRET THESE NUMBERS:")
    print("="*60)
    print("1. Term Frequency (TF): Local Importance")
    print("   - Measures how often a word appears in a specific document.")
    print("   - Higher TF = The word is a major topic within that single sentence.")
    print("\n2. Inverse Document Frequency (IDF): Global Rarity")
    print("   - Measures how rare a word is across ALL documents.")
    print("   - If a word is in EVERY document (like 'the' or 'is'), IDF becomes 0.")
    print("   - If a word is only in ONE document (like 'neural'), IDF becomes high.")
    print("\n3. The Final TF-IDF Score: The Sweet Spot")
    print("   - High Score: The word is very common in this specific document, ")
    print("                 but very rare everywhere else. This means it is a ")
    print("                 highly relevant keyword that defines this document!")
    print("   - Low Score (near 0): The word either rarely appears in this document,")
    print("                         or it appears so often in ALL documents that it")
    print("                         carries no special meaning.")
    print("="*60 + "\n")

# Example usage with a larger, custom dataset
if __name__ == "__main__":
    # A larger custom dataset to show how word rarity affects the math
    documents = [
        "Machine learning teaches a machine to learn.",
        "Deep learning is a subset of machine learning.",
        "Artificial intelligence includes both machine learning and deep learning.",
        "A neural network is used in deep learning."
    ]
    print(documents[0])
    print(documents[1])
    print(documents[2])
    print(documents[3])
    
    vectorizer = TFIDFVectorizer(use_smoothing=False)
    tfidf = vectorizer.fit_transform(documents)

    print("\nTF-IDF Results with Step-by-Step Calculation:\n")
    print("-" * 60)
    
    for i, scores in enumerate(tfidf):
        print(f"Doc {i+1}: '{documents[i]}'")
        
        tokens = vectorizer.tokenized_docs[i]
        total_terms_in_doc = len(tokens)
        total_docs = len(vectorizer.tokenized_docs)
        
        # Sort terms by score to get the top 2 defining keywords for each doc
        top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:2]
        
        for term, final_score in top:
            if final_score > 0:
                tf_val = vectorizer.tf_matrix[i].get(term, 0)
                idf_val = vectorizer.idf_values.get(term, 0)
                
                term_count_in_doc = tokens.count(term)
                docs_with_term = sum(1 for doc in vectorizer.tokenized_docs if term in doc)
                
                print(f"\n  Keyword: '{term}'")
                print(f"    TF  = {term_count_in_doc}/{total_terms_in_doc} = {tf_val:.4f}")
                print(f"    IDF = log10({total_docs}/{docs_with_term}) = {idf_val:.4f}")
                print(f"    TF-IDF = {tf_val:.4f} * {idf_val:.4f} = {final_score:.4f}")
        
        print("-" * 60)
        
    # Run the explanation guide at the very end
    explain_interpretation()