"""
Vector Embedding Visualization Module

Provides functions to visualize word embeddings and vectors using
dimensionality reduction techniques (PCA, t-SNE, UMAP).
"""

import numpy as np
import json
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Try to import optional visualization libraries
try:
    from sklearn.manifold import TSNE
    HAS_TSNE = True
except ImportError:
    HAS_TSNE = False

try:
    import umap
    HAS_UMAP = True
except ImportError:
    HAS_UMAP = False


def reduce_to_2d(vectors, method='pca', perplexity=5, random_state=42):
    """
    Reduce high-dimensional vectors to 2D for visualization.
    
    Args:
        vectors: numpy array of shape (n_samples, n_features)
        method: 'pca', 'tsne', or 'umap'
        perplexity: perplexity for t-SNE (used if method='tsne')
        random_state: random seed for reproducibility
    
    Returns:
        2D numpy array of shape (n_samples, 2)
    """
    if len(vectors.shape) != 2 or vectors.shape[1] < 2:
        raise ValueError("Input must be 2D array with at least 2 features")
    
    # Standardize features
    scaler = StandardScaler()
    vectors_scaled = scaler.fit_transform(vectors)
    
    if method == 'pca':
        # Use PCA for 2D projection
        pca = PCA(n_components=2, random_state=random_state)
        return pca.fit_transform(vectors_scaled)
    
    elif method == 'tsne':
        if not HAS_TSNE:
            print("Warning: scikit-learn TSNE not available, falling back to PCA")
            return reduce_to_2d(vectors, method='pca', random_state=random_state)
        
        # Adjust perplexity based on sample size
        n_samples = vectors.shape[0]
        perp = min(perplexity, (n_samples - 1) // 3)
        
        tsne = TSNE(n_components=2, perplexity=perp, random_state=random_state, n_iter=1000)
        return tsne.fit_transform(vectors_scaled)
    
    elif method == 'umap':
        if not HAS_UMAP:
            print("Warning: UMAP not available, falling back to PCA")
            return reduce_to_2d(vectors, method='pca', random_state=random_state)
        
        reducer = umap.UMAP(n_components=2, random_state=random_state)
        return reducer.fit_transform(vectors_scaled)
    
    else:
        raise ValueError(f"Unknown method: {method}. Choose 'pca', 'tsne', or 'umap'")


def visualize_tfidf_vectors(tfidf_model, documents, method='pca'):
    """
    Visualize TF-IDF document vectors in 2D space.
    
    Args:
        tfidf_model: TF-IDF model with transform method
        documents: list of document strings
        method: dimensionality reduction method
    
    Returns:
        dict with visualization data (plotly format)
    """
    try:
        # Tokenize documents
        tokenized_docs = [doc.lower().split() for doc in documents]
        
        # Compute TF-IDF vectors
        tfidf_vectors = []
        vocab_size = len(tfidf_model.vocab)
        
        for doc in tokenized_docs:
            tfidf_vec = np.zeros(vocab_size)
            
            # Compute term frequencies
            word_freq = {}
            for word in doc:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            total_words = len(doc)
            
            # Compute TF-IDF for each word
            for word, freq in word_freq.items():
                if word in tfidf_model.vocab:
                    idx = tfidf_model.vocab[word]
                    tf = freq / total_words
                    idf = tfidf_model.idf.get(word, 0)
                    tfidf_vec[idx] = tf * idf
            
            tfidf_vectors.append(tfidf_vec)
        
        tfidf_vectors = np.array(tfidf_vectors)
        
        # Reduce to 2D
        points_2d = reduce_to_2d(tfidf_vectors, method=method)
        
        # Prepare data for plotly
        viz_data = {
            'type': 'scatter',
            'method': method,
            'points': [
                {
                    'x': float(points_2d[i, 0]),
                    'y': float(points_2d[i, 1]),
                    'label': f'Doc {i+1}',
                    'text': documents[i][:50] + ('...' if len(documents[i]) > 50 else '')
                }
                for i in range(len(documents))
            ],
            'title': f'TF-IDF Document Vectors ({method.upper()})',
            'x_label': 'Dimension 1',
            'y_label': 'Dimension 2'
        }
        
        return viz_data
    
    except Exception as e:
        return {'error': str(e), 'type': 'tfidf_visualization'}


def visualize_sgns_embeddings(sgns_model, method='pca'):
    """
    Visualize SGNS word embeddings in 2D space.
    
    Args:
        sgns_model: SkipGramNegativeSampling model with trained embeddings
        method: dimensionality reduction method
    
    Returns:
        dict with visualization data (plotly format)
    """
    try:
        if sgns_model.word_vectors is None:
            return {'error': 'Model not trained yet', 'type': 'sgns_visualization'}
        
        # Get embeddings
        word_vectors = sgns_model.word_vectors
        words = sorted(sgns_model.vocab.keys())
        
        # Reduce to 2D
        points_2d = reduce_to_2d(word_vectors, method=method)
        
        # Prepare data for plotly
        viz_data = {
            'type': 'scatter',
            'method': method,
            'points': [
                {
                    'x': float(points_2d[i, 0]),
                    'y': float(points_2d[i, 1]),
                    'label': words[i],
                    'text': words[i]
                }
                for i in range(len(words))
            ],
            'title': f'SGNS Word Embeddings ({method.upper()})',
            'x_label': 'Dimension 1',
            'y_label': 'Dimension 2',
            'vocab_size': len(words),
            'embedding_dim': sgns_model.embedding_dim
        }
        
        return viz_data
    
    except Exception as e:
        return {'error': str(e), 'type': 'sgns_visualization'}


def compute_similarity_matrix(vectors, labels=None):
    """
    Compute cosine similarity matrix between vectors.
    
    Args:
        vectors: numpy array of shape (n_samples, n_features)
        labels: optional list of labels for vectors
    
    Returns:
        dict with similarity matrix data
    """
    try:
        # Normalize vectors
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        vectors_normalized = vectors / (norms + 1e-10)
        
        # Compute cosine similarity
        similarity_matrix = np.dot(vectors_normalized, vectors_normalized.T)
        
        # Prepare data
        n = similarity_matrix.shape[0]
        if labels is None:
            labels = [f'Item {i}' for i in range(n)]
        
        return {
            'matrix': similarity_matrix.tolist(),
            'labels': labels,
            'title': 'Cosine Similarity Matrix'
        }
    
    except Exception as e:
        return {'error': str(e)}


def get_most_similar_words(sgns_model, word, topn=5):
    """
    Find most similar words to a given word using cosine similarity.
    
    Args:
        sgns_model: SkipGramNegativeSampling model
        word: target word
        topn: number of similar words to return
    
    Returns:
        list of (word, similarity_score) tuples
    """
    try:
        if word not in sgns_model.vocab:
            return {'error': f"Word '{word}' not in vocabulary"}
        
        return {
            'word': word,
            'similar': sgns_model.most_similar(word, topn=topn)
        }
    
    except Exception as e:
        return {'error': str(e)}


def create_plotly_scatter(data_dict):
    """
    Convert visualization data dict to Plotly JSON.
    
    Args:
        data_dict: dict with visualization data from visualize_* functions
    
    Returns:
        plotly JSON object
    """
    try:
        if 'error' in data_dict:
            return None
        
        points = data_dict.get('points', [])
        title = data_dict.get('title', 'Visualization')
        x_label = data_dict.get('x_label', 'X')
        y_label = data_dict.get('y_label', 'Y')
        
        # Extract coordinates
        xs = [p['x'] for p in points]
        ys = [p['y'] for p in points]
        labels = [p['label'] for p in points]
        texts = [p['text'] for p in points]
        
        plotly_json = {
            'data': [{
                'x': xs,
                'y': ys,
                'mode': 'markers+text',
                'type': 'scatter',
                'marker': {
                    'size': 10,
                    'color': list(range(len(xs))),
                    'colorscale': 'Viridis',
                    'showscale': True
                },
                'text': labels,
                'textposition': 'top center',
                'hovertext': texts,
                'hoverinfo': 'text'
            }],
            'layout': {
                'title': title,
                'xaxis': {'title': x_label},
                'yaxis': {'title': y_label},
                'hovermode': 'closest',
                'width': 900,
                'height': 700,
                'margin': {'l': 100, 'r': 100, 'b': 100, 't': 100}
            }
        }
        
        return plotly_json
    
    except Exception as e:
        return None
