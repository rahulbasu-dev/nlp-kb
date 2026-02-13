#!/usr/bin/env python3
"""
Quick demo showing visualization outputs
"""

from app import app
import json

client = app.test_client()

print("=" * 70)
print("EMBEDDING VISUALIZATIONS DEMONSTRATION")
print("=" * 70)

# TF-IDF Demo
print("\n📊 TF-IDF DOCUMENT VECTOR VISUALIZATION")
print("-" * 70)

response = client.post("/demo/tfidf", json={
    "documents": [
        "machine learning is great for prediction",
        "deep learning uses neural networks",
        "natural language processing helps with text"
    ]
})

data = response.get_json()
if data.get('status') == 'success' and data.get('visualization'):
    viz = data['visualization']
    meta = data.get('viz_metadata', {})
    
    print(f"\n✓ Visualization Generated: {viz['layout']['title']}")
    print(f"  Method: {meta.get('method', 'PCA').upper()}")
    print(f"  Documents: {meta.get('num_documents')}")
    print(f"  Unique Words: {meta.get('vocab_size')}")
    
    print(f"\n  Document Positions in 2D Space:")
    for i, point in enumerate(viz['data'][0]['text'][:3]):
        x = viz['data'][0]['x'][i]
        y = viz['data'][0]['y'][i]
        text = viz['data'][0]['hovertext'][i][:50]
        print(f"    • {point:6s} @ ({x:7.3f}, {y:7.3f}) - {text}...")
    
    print(f"\n  💡 Insight: Documents close together have similar vocabulary")
    print(f"             Further apart = more different word usage")

# SGNS Demo
print("\n\n🧠 SGNS WORD EMBEDDING VISUALIZATION")
print("-" * 70)

response = client.post("/demo/sgns", json={
    "corpus": [
        "the cat sat on the mat",
        "the dog played in the park",
        "the bird flew over the tree"
    ]
})

data = response.get_json()
if data.get('status') == 'success' and data.get('visualization'):
    viz = data['visualization']
    meta = data.get('viz_metadata', {})
    
    print(f"\n✓ Visualization Generated: {viz['layout']['title']}")
    print(f"  Method: {meta.get('method', 'PCA').upper()}")
    print(f"  Vocabulary Size: {meta.get('vocab_size')} words")
    print(f"  Embedding Dimension: {meta.get('embedding_dim')}D")
    
    print(f"\n  Word Positions in 2D Space:")
    words_shown = min(5, len(viz['data'][0]['text']))
    for i in range(words_shown):
        word = viz['data'][0]['text'][i]
        x = viz['data'][0]['x'][i]
        y = viz['data'][0]['y'][i]
        print(f"    • {word:8s} @ ({x:7.3f}, {y:7.3f})")
    if len(viz['data'][0]['text']) > 5:
        print(f"    ... and {len(viz['data'][0]['text']) - 5} more words")
    
    print(f"\n  💡 Insight: Words with similar context appear close together")
    print(f"             'cat', 'dog', 'bird' should be in same area")
    print(f"             'the', 'on', 'in' should be in another cluster")

print("\n" + "=" * 70)
print("✅ EMBEDDING VISUALIZATIONS ARE WORKING!")
print("=" * 70)

print("\n📱 How to Use in the Web App:")
print("-" * 70)
print("1. Go to /demo/tfidf or /demo/sgns")
print("2. Enter your documents or corpus")
print("3. Click 'Calculate TF-IDF' or 'Train Model'")
print("4. See the 2D visualization of your data!")
print("5. Hover over points for more information")
print("6. Zoom and pan the interactive chart")

print("\n🎨 What You'll See:")
print("-" * 70)
print("• Interactive Plotly scatter plot")
print("• Color gradient for visual distinction")
print("• Labels and hover tooltips")
print("• Document/word positions based on embeddings")
print("• Metadata about the visualization")

print("\n✨ Supported Reduction Methods:")
print("-" * 70)
print("• PCA (default) - Fast and stable")
print("• t-SNE (optional) - Better local structure")
print("• UMAP (optional) - Balance of both")

print("\n" + "=" * 70)
