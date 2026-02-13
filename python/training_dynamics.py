"""
Training Dynamics Visualization Module

Tracks how word vectors evolve during SGNS training, showing:
- How similar vectors move closer together
- How negative samples are pushed farther apart
- The learning progression over epochs
"""

import numpy as np
import json
from embeddings_viz import reduce_to_2d


def identify_positive_word_pairs(sentences, window_size=2):
    """
    Identify positive word pairs from corpus (actual context words).
    
    Args:
        sentences: list of sentences (each sentence is list of words)
        window_size: context window size
    
    Returns:
        set of frozensets containing positive (target, context) word pairs
    """
    positive_pairs = set()
    
    for sentence in sentences:
        for target_pos, target_word in enumerate(sentence):
            context_start = max(0, target_pos - window_size)
            context_end = min(len(sentence), target_pos + window_size + 1)
            
            for context_pos in range(context_start, context_end):
                if context_pos == target_pos:
                    continue
                context_word = sentence[context_pos]
                # Store as frozenset for unordered pair comparison
                pair = frozenset([target_word, context_word])
                positive_pairs.add(pair)
    
    return positive_pairs


def extract_training_snapshots(model, sentences, epochs=5, capture_interval=1):
    """
    Train SGNS model while capturing vector snapshots at each epoch.
    
    Args:
        model: SkipGramNegativeSampling model (untrained)
        sentences: training corpus
        epochs: number of epochs to train
        capture_interval: capture snapshot every N epochs
    
    Returns:
        dict with:
        - 'snapshots': list of vector states at each checkpoint
        - 'epoch_indices': which epochs these snapshots represent
        - 'vocab': word -> index mapping
        - 'sorted_words': sorted word list for consistent ordering
        - 'positive_pairs': set of positive word pairs from corpus
    """
    # Build vocab
    model.build_vocab(sentences)
    vocab_size = len(model.vocab)
    sorted_words = sorted(model.vocab.keys())
    
    # Identify positive pairs from corpus
    positive_pairs = identify_positive_word_pairs(sentences, model.window_size)
    
    snapshots = []
    epoch_indices = []
    
    # Capture initial vectors (epoch 0)
    initial_state = {
        'epoch': 0,
        'word_vectors': model.word_vectors.copy(),
        'context_vectors': model.context_vectors.copy(),
    }
    snapshots.append(initial_state)
    epoch_indices.append(0)
    
    # Training loop with snapshots
    print(f"[Training] Epochs: {epochs}, Capture interval: {capture_interval}")
    
    for epoch in range(epochs):
        pair_count = 0
        
        for sentence in sentences:
            for target_pos, target_word in enumerate(sentence):
                context_start = max(0, target_pos - model.window_size)
                context_end = min(len(sentence), target_pos + model.window_size + 1)
                
                target_idx = model.vocab[target_word]
                
                for context_pos in range(context_start, context_end):
                    if context_pos == target_pos:
                        continue
                    
                    context_word = sentence[context_pos]
                    context_idx = model.vocab[context_word]
                    
                    model._train_pair(target_idx, context_idx)
                    pair_count += 1
        
        print(f"  Epoch {epoch + 1}/{epochs}: {pair_count} word pairs")
        
        # Capture snapshot if at capture interval
        if (epoch + 1) % capture_interval == 0:
            snapshot = {
                'epoch': epoch + 1,
                'word_vectors': model.word_vectors.copy(),
                'context_vectors': model.context_vectors.copy(),
            }
            snapshots.append(snapshot)
            epoch_indices.append(epoch + 1)
    
    return {
        'snapshots': snapshots,
        'epoch_indices': epoch_indices,
        'vocab': model.vocab,
        'sorted_words': sorted_words,
        'embedding_dim': model.embedding_dim,
        'positive_pairs': positive_pairs,
    }


def compute_pairwise_distances(vectors, sorted_words):
    """
    Compute pairwise distances between all word vectors.
    
    Args:
        vectors: (vocab_size, embedding_dim) array
        sorted_words: list of word strings
    
    Returns:
        dict mapping word pairs to their cosine distances
    """
    # Normalize vectors
    vectors_norm = vectors / (np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-10)
    
    # Compute pairwise distances
    distances = {}
    for i, word1 in enumerate(sorted_words):
        for j, word2 in enumerate(sorted_words):
            if i < j:
                # Cosine distance = 1 - cosine similarity
                similarity = np.dot(vectors_norm[i], vectors_norm[j])
                distance = 1.0 - similarity
                distances[f"{word1}|{word2}"] = float(distance)
    
    return distances


def create_animation_frames(training_data, method='pca'):
    """
    Create Plotly animation frames showing vector evolution.
    Highlights negative samples with distinct marker styling.
    
    Args:
        training_data: output from extract_training_snapshots()
        method: 'pca', 'tsne', or 'umap'
    
    Returns:
        dict with Plotly animation structure:
        - frames: list of frame objects (one per epoch)
        - layout: animation layout settings
        - data: initial data
    """
    snapshots = training_data['snapshots']
    epoch_indices = training_data['epoch_indices']
    sorted_words = training_data['sorted_words']
    positive_pairs = training_data['positive_pairs']
    
    frames = []
    
    # Process each snapshot
    for snap_idx, snapshot in enumerate(snapshots):
        epoch = epoch_indices[snap_idx]
        vectors = snapshot['word_vectors']
        
        # Reduce to 2D
        coords_2d = reduce_to_2d(vectors, method=method)
        
        # Determine if each word appears in negative samples (words that are NOT in positive pairs)
        # Build set of all words that appear in positive pairs
        positive_words = set()
        for pair in positive_pairs:
            positive_words.update(pair)
        
        # Words that don't appear in positive pairs are primarily negative samples
        negative_sample_words = set(sorted_words) - positive_words
        
        # Create marker colors: green for positive, red for negative/context
        marker_colors = []
        marker_symbols = []
        marker_sizes = []
        
        for word in sorted_words:
            if word in negative_sample_words and len(negative_sample_words) > 0:
                # Negative samples: red with X marker
                marker_colors.append('red')
                marker_symbols.append('x')
                marker_sizes.append(12)
            else:
                # Positive samples: teal with circle
                marker_colors.append('teal')
                marker_symbols.append('circle')
                marker_sizes.append(10)
        
        # Create frame data with multiple traces (one per marker type)
        # Positive trace
        positive_mask = [word not in negative_sample_words or len(negative_sample_words) == 0 for word in sorted_words]
        positive_indices = [i for i, m in enumerate(positive_mask) if m]
        
        frame_data = []
        
        # Add positive samples trace
        if positive_indices:
            pos_x = [coords_2d[i, 0] for i in positive_indices]
            pos_y = [coords_2d[i, 1] for i in positive_indices]
            pos_text = [sorted_words[i] for i in positive_indices]
            
            frame_data.append({
                'x': pos_x,
                'y': pos_y,
                'text': pos_text,
                'mode': 'markers+text',
                'type': 'scatter',
                'marker': {
                    'size': 10,
                    'color': 'teal',
                    'opacity': 0.8,
                    'line': {'width': 2, 'color': 'white'}
                },
                'textposition': 'top center',
                'textfont': {'size': 10},
                'hovertemplate': '<b>%{text}</b> (Positive)<br>X: %{x:.3f}<br>Y: %{y:.3f}<extra></extra>',
                'name': 'Positive Samples'
            })
        
        # Add negative samples trace
        negative_indices = [i for i, m in enumerate(positive_mask) if not m and len(negative_sample_words) > 0]
        if negative_indices:
            neg_x = [coords_2d[i, 0] for i in negative_indices]
            neg_y = [coords_2d[i, 1] for i in negative_indices]
            neg_text = [sorted_words[i] for i in negative_indices]
            
            frame_data.append({
                'x': neg_x,
                'y': neg_y,
                'text': neg_text,
                'mode': 'markers+text',
                'type': 'scatter',
                'marker': {
                    'size': 12,
                    'color': 'red',
                    'symbol': 'x',
                    'line': {'width': 2}
                },
                'textposition': 'bottom center',
                'textfont': {'size': 10, 'color': 'red'},
                'hovertemplate': '<b>%{text}</b> (Negative)<br>X: %{x:.3f}<br>Y: %{y:.3f}<extra></extra>',
                'name': 'Negative Samples'
            })
        
        frames.append({
            'data': frame_data,
            'name': f'Epoch {epoch}'
        })
    
    # Initial frame (epoch 0)
    initial_vectors = snapshots[0]['word_vectors']
    initial_coords = reduce_to_2d(initial_vectors, method=method)
    
    positive_words = set()
    for pair in positive_pairs:
        positive_words.update(pair)
    negative_sample_words = set(sorted_words) - positive_words
    positive_mask = [word not in negative_sample_words or len(negative_sample_words) == 0 for word in sorted_words]
    
    initial_data = []
    
    # Positive samples
    positive_indices = [i for i, m in enumerate(positive_mask) if m]
    if positive_indices:
        pos_x = [initial_coords[i, 0] for i in positive_indices]
        pos_y = [initial_coords[i, 1] for i in positive_indices]
        pos_text = [sorted_words[i] for i in positive_indices]
        
        initial_data.append({
            'x': pos_x,
            'y': pos_y,
            'text': pos_text,
            'mode': 'markers+text',
            'type': 'scatter',
            'marker': {
                'size': 10,
                'color': 'teal',
                'opacity': 0.8,
                'line': {'width': 2, 'color': 'white'}
            },
            'textposition': 'top center',
            'textfont': {'size': 10},
            'hovertemplate': '<b>%{text}</b> (Positive)<br>X: %{x:.3f}<br>Y: %{y:.3f}<extra></extra>',
            'name': 'Positive Samples'
        })
    
    # Negative samples
    negative_indices = [i for i, m in enumerate(positive_mask) if not m and len(negative_sample_words) > 0]
    if negative_indices:
        neg_x = [initial_coords[i, 0] for i in negative_indices]
        neg_y = [initial_coords[i, 1] for i in negative_indices]
        neg_text = [sorted_words[i] for i in negative_indices]
        
        initial_data.append({
            'x': neg_x,
            'y': neg_y,
            'text': neg_text,
            'mode': 'markers+text',
            'type': 'scatter',
            'marker': {
                'size': 12,
                'color': 'red',
                'symbol': 'x',
                'line': {'width': 2}
            },
            'textposition': 'bottom center',
            'textfont': {'size': 10, 'color': 'red'},
            'hovertemplate': '<b>%{text}</b> (Negative)<br>X: %{x:.3f}<br>Y: %{y:.3f}<extra></extra>',
            'name': 'Negative Samples'
        })
    
    layout = {
        'title': f'SGNS Training Dynamics (Dimensionality Reduction: {method.upper()})<br><sub>🔷 Teal = Positive samples (in corpus) | 🔶 Red X = Negative samples (randomly sampled)</sub>',
        'xaxis': {'title': 'Dimension 1'},
        'yaxis': {'title': 'Dimension 2'},
        'height': 600,
        'hovermode': 'closest',
        'showlegend': True,
        'updatemenus': [{
            'type': 'buttons',
            'showactive': False,
            'buttons': [
                {
                    'label': '▶ Play',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 800, 'redraw': True},
                        'fromcurrent': True,
                        'transition': {'duration': 400}
                    }]
                },
                {
                    'label': '⏸ Pause',
                    'method': 'animate',
                    'args': [[None], {
                        'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                }
            ]
        }],
        'sliders': [{
            'active': 0,
            'yanchor': 'top',
            'y': 0,
            'xanchor': 'left',
            'x': 0.1,
            'len': 0.9,
            'transition': {'duration': 300},
            'pad': {'b': 10, 't': 50},
            'currentvalue': {
                'prefix': 'Epoch: ',
                'visible': True,
                'xanchor': 'right',
                'font': {'size': 16}
            },
            'steps': [
                {
                    'args': [[f['name']], {
                        'frame': {'duration': 300, 'redraw': True},
                        'mode': 'immediate',
                        'transition': {'duration': 300}
                    }],
                    'method': 'animate',
                    'label': f['name']
                }
                for f in frames
            ]
        }]
    }
    
    return {
        'data': initial_data,
        'frames': frames,
        'layout': layout
    }


def create_distance_progression(training_data):
    """
    Create visualization showing how distances between word pairs change over time.
    
    Args:
        training_data: output from extract_training_snapshots()
    
    Returns:
        dict with Plotly line chart showing distance evolution
    """
    snapshots = training_data['snapshots']
    epoch_indices = training_data['epoch_indices']
    sorted_words = training_data['sorted_words']
    
    # Select word pairs to track (similar and dissimilar)
    similar_pairs = [
        (0, 1) if len(sorted_words) > 1 else None,
        (0, 2) if len(sorted_words) > 2 else None,
    ]
    similar_pairs = [p for p in similar_pairs if p is not None]
    
    traces = []
    
    # Track distances for each pair over epochs
    for pair_idx, (word_i, word_j) in enumerate(similar_pairs):
        word1 = sorted_words[word_i]
        word2 = sorted_words[word_j]
        
        distances = []
        for snapshot in snapshots:
            vectors = snapshot['word_vectors']
            v1 = vectors[word_i]
            v2 = vectors[word_j]
            
            # Cosine distance
            dist = 1.0 - (np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-10))
            distances.append(float(dist))
        
        trace = {
            'x': epoch_indices,
            'y': distances,
            'name': f'{word1} ↔ {word2}',
            'mode': 'lines+markers',
            'type': 'scatter'
        }
        traces.append(trace)
    
    layout = {
        'title': 'Word Pair Distance Evolution During Training',
        'xaxis': {'title': 'Epoch'},
        'yaxis': {'title': 'Cosine Distance (1 - similarity)'},
        'hovermode': 'x unified',
        'height': 500
    }
    
    return {
        'data': traces,
        'layout': layout
    }


def create_similarity_heatmap_evolution(training_data, selected_words=None):
    """
    Create visualization showing how word similarity matrix evolves.
    Highlights negative sample pairs (words not in corpus together).
    
    Args:
        training_data: output from extract_training_snapshots()
        selected_words: list of words to track (default: all)
    
    Returns:
        dict with multiple heatmap snapshots (frames for animation)
    """
    snapshots = training_data['snapshots']
    epoch_indices = training_data['epoch_indices']
    sorted_words = training_data['sorted_words']
    positive_pairs = training_data['positive_pairs']
    
    # Select subset of words if specified
    if selected_words is None:
        selected_words = sorted_words[:min(10, len(sorted_words))]
    
    word_indices = [i for i, w in enumerate(sorted_words) if w in selected_words]
    selected_words = [sorted_words[i] for i in word_indices]
    
    # Build set of negative pairs (words NOT in positive pairs)
    negative_pairs = set()
    for i in range(len(selected_words)):
        for j in range(i + 1, len(selected_words)):
            pair = frozenset([selected_words[i], selected_words[j]])
            if pair not in positive_pairs:
                negative_pairs.add(pair)
    
    frames = []
    
    for snap_idx, snapshot in enumerate(snapshots):
        epoch = epoch_indices[snap_idx]
        vectors = snapshot['word_vectors']
        
        # Compute similarity matrix
        selected_vectors = vectors[word_indices]
        vectors_norm = selected_vectors / (np.linalg.norm(selected_vectors, axis=1, keepdims=True) + 1e-10)
        similarity_matrix = np.dot(vectors_norm, vectors_norm.T)
        
        # Create custom hover text showing pair type
        hover_text = []
        for i in range(len(selected_words)):
            row = []
            for j in range(len(selected_words)):
                word1, word2 = selected_words[i], selected_words[j]
                pair = frozenset([word1, word2])
                is_negative = pair in negative_pairs if i != j else False
                pair_type = "Negative" if is_negative else ("Positive" if i != j else "Same")
                row.append(f"{word1} ↔ {word2}: {similarity_matrix[i, j]:.3f} ({pair_type})")
            hover_text.append(row)
        
        frame_data = {
            'z': similarity_matrix.tolist(),
            'x': selected_words,
            'y': selected_words,
            'type': 'heatmap',
            'colorscale': 'RdBu',
            'zmid': 0,
            'zmin': -1,
            'zmax': 1,
            'colorbar': {'title': 'Cosine<br>Similarity'},
            'customdata': np.array(hover_text),
            'hovertemplate': '%{customdata}<extra></extra>',
            'name': f'Epoch {epoch}'
        }
        
        frames.append({
            'data': [frame_data],
            'name': f'Epoch {epoch}'
        })
    
    # Initial frame
    initial_vectors = snapshots[0]['word_vectors']
    initial_selected = initial_vectors[word_indices]
    initial_norm = initial_selected / (np.linalg.norm(initial_selected, axis=1, keepdims=True) + 1e-10)
    initial_similarity = np.dot(initial_norm, initial_norm.T)
    
    # Initial hover text
    initial_hover = []
    for i in range(len(selected_words)):
        row = []
        for j in range(len(selected_words)):
            word1, word2 = selected_words[i], selected_words[j]
            pair = frozenset([word1, word2])
            is_negative = pair in negative_pairs if i != j else False
            pair_type = "Negative" if is_negative else ("Positive" if i != j else "Same")
            row.append(f"{word1} ↔ {word2}: {initial_similarity[i, j]:.3f} ({pair_type})")
        initial_hover.append(row)
    
    initial_data = [{
        'z': initial_similarity.tolist(),
        'x': selected_words,
        'y': selected_words,
        'type': 'heatmap',
        'colorscale': 'RdBu',
        'zmid': 0,
        'zmin': -1,
        'zmax': 1,
        'colorbar': {'title': 'Cosine<br>Similarity'},
        'customdata': np.array(initial_hover),
        'hovertemplate': '%{customdata}<extra></extra>',
        'name': 'Epoch 0'
    }]
    
    layout = {
        'title': f'Word Similarity Matrix Evolution During SGNS Training<br><sub>Red (negative) = words randomly sampled together | Blue (positive) = words from corpus</sub>',
        'height': 600,
        'updatemenus': [{
            'type': 'buttons',
            'showactive': False,
            'buttons': [
                {
                    'label': '▶ Play',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 1000, 'redraw': True},
                        'fromcurrent': True,
                        'transition': {'duration': 500}
                    }]
                },
                {
                    'label': '⏸ Pause',
                    'method': 'animate',
                    'args': [[None], {
                        'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                }
            ]
        }],
        'sliders': [{
            'active': 0,
            'yanchor': 'top',
            'y': 0,
            'xanchor': 'left',
            'x': 0.1,
            'len': 0.9,
            'transition': {'duration': 500},
            'pad': {'b': 10, 't': 50},
            'currentvalue': {
                'prefix': 'Epoch: ',
                'visible': True,
                'xanchor': 'right',
                'font': {'size': 16}
            },
            'steps': [
                {
                    'args': [[f['name']], {
                        'frame': {'duration': 500, 'redraw': True},
                        'mode': 'immediate',
                        'transition': {'duration': 500}
                    }],
                    'method': 'animate',
                    'label': f['name']
                }
                for f in frames
            ]
        }]
    }
    
    return {
        'data': initial_data,
        'frames': frames,
        'layout': layout
    }
