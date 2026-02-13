"""
NLP Classroom - Flask Web Application
A modular, scalable web interface for teaching NLP concepts
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
import os
import json
from pathlib import Path
import subprocess
import sys

# Import our models
from sgns import SkipGramNegativeSampling, TFIDF
from embeddings_viz import (
    visualize_tfidf_vectors, 
    visualize_sgns_embeddings, 
    compute_similarity_matrix, 
    create_plotly_scatter
)
from training_dynamics import (
    extract_training_snapshots,
    create_animation_frames,
    create_distance_progression,
    create_similarity_heatmap_evolution
)

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SECRET_KEY'] = 'nlp-classroom-2026'
app.config['VISUALIZATIONS_FOLDER'] = '../static/visualizations'
app.config['STATIC_FOLDER'] = '../static'

# Ensure static directories exist
os.makedirs('../static/visualizations', exist_ok=True)
os.makedirs('../static/css', exist_ok=True)
os.makedirs('../static/js', exist_ok=True)

# ============================================================================
# ROUTE: Home Page
# ============================================================================

@app.route('/')
def index():
    """Main landing page with lesson navigation."""
    return render_template('index.html')

# ============================================================================
# ROUTE: Lesson Pages
# ============================================================================

@app.route('/lessons/tfidf')
def lesson_tfidf():
    """TF-IDF lesson page with interactive components."""
    visualizations = [
        {'file': '01_tfidf_matrix.png', 'title': 'Document-Term Matrix', 
         'description': 'TF-IDF scores for each word in each document'},
        {'file': '02_idf_distribution.png', 'title': 'IDF Distribution', 
         'description': 'Word importance based on rarity'},
        {'file': '03_tfidf_similarities.png', 'title': 'Document Similarity', 
         'description': 'Comparing documents using TF-IDF'},
    ]
    return render_template('lesson_tfidf.html', visualizations=visualizations)

@app.route('/lessons/sgns')
def lesson_sgns():
    """SGNS lesson page with interactive components."""
    visualizations = [
        {'file': '05_context_window.png', 'title': 'Context Window', 
         'description': 'How the sliding window captures word relationships'},
        {'file': '06_sampling_process.png', 'title': 'Negative Sampling', 
         'description': 'Efficient training with positive and negative samples'},
        {'file': '07_embeddings_2d.png', 'title': 'Word Embeddings Space', 
         'description': 'Learned word relationships visualized in 2D'},
        {'file': '08_similarity_heatmap.png', 'title': 'Similarity Matrix', 
         'description': 'Quantified word-to-word similarities'},
        {'file': '09_algorithm_steps.png', 'title': 'Algorithm Flow', 
         'description': 'Step-by-step SGNS algorithm'},
        {'file': '10_training_dynamics.png', 'title': 'Training Progress', 
         'description': 'How embeddings improve over epochs'},
    ]
    return render_template('lesson_sgns.html', visualizations=visualizations)

@app.route('/lessons/comparison')
def lesson_comparison():
    """Comparison lesson showing both methods side-by-side."""
    return render_template('lesson_comparison.html')

# ============================================================================
# ROUTE: Interactive Demos
# ============================================================================

@app.route('/demo/tfidf', methods=['GET', 'POST'])
def demo_tfidf():
    """Interactive TF-IDF demo."""
    if request.method == 'POST':
        documents = request.json.get('documents', [])
        if documents:
            result = run_tfidf_demo(documents)
            return jsonify(result)
    return render_template('demo_tfidf.html')

@app.route('/demo/sgns', methods=['GET', 'POST'])
def demo_sgns():
    """Interactive SGNS demo."""
    if request.method == 'POST':
        corpus = request.json.get('corpus', [])
        params = request.json.get('params', {})
        if corpus:
            result = run_sgns_demo(corpus, params)
            return jsonify(result)
    return render_template('demo_sgns.html')

@app.route('/demo/sgns-training-dynamics', methods=['GET', 'POST'])
def demo_sgns_training_dynamics():
    """Interactive SGNS training dynamics visualization."""
    if request.method == 'POST':
        corpus = request.json.get('corpus', [])
        params = request.json.get('params', {})
        viz_type = request.json.get('viz_type', 'animation')
        
        if corpus and len(corpus) > 0:
            try:
                # Tokenize corpus
                sentences = [sent.lower().split() for sent in corpus]
                sentences = [s for s in sentences if len(s) > 0]  # Filter empty
                
                if not sentences:
                    return jsonify({'error': 'No valid sentences in corpus'}), 400
                
                # Initialize and train model while capturing snapshots
                model = SkipGramNegativeSampling(
                    embedding_dim=params.get('embedding_dim', 50),
                    learning_rate=params.get('learning_rate', 0.025),
                    negative_samples=params.get('negative_samples', 5),
                    window_size=params.get('window_size', 2)
                )
                
                epochs = params.get('epochs', 10)
                capture_interval = params.get('capture_interval', 1)
                method = params.get('method', 'pca')
                
                print(f"[Training] Starting with {len(sentences)} sentences, {epochs} epochs")
                training_data = extract_training_snapshots(model, sentences, epochs=epochs, capture_interval=capture_interval)
                
                # Generate requested visualization
                if viz_type == 'animation':
                    viz = create_animation_frames(training_data, method=method)
                elif viz_type == 'distance':
                    viz = create_distance_progression(training_data)
                elif viz_type == 'heatmap':
                    viz = create_similarity_heatmap_evolution(training_data)
                else:
                    viz = create_animation_frames(training_data, method=method)
                
                return jsonify({
                    'status': 'success',
                    'visualization': viz,
                    'viz_type': viz_type,
                    'metadata': {
                        'vocab_size': len(training_data['sorted_words']),
                        'epochs': epochs,
                        'method': method,
                        'embedding_dim': training_data['embedding_dim']
                    }
                })
            except Exception as e:
                print(f"Error: {str(e)}")
                import traceback
                traceback.print_exc()
                return jsonify({'error': str(e)}), 500
    
    return render_template('demo_sgns_dynamics.html')

# ============================================================================
# ROUTE: Visualizations Gallery
# ============================================================================

@app.route('/visualizations')
def visualizations_gallery():
    """Gallery view of all visualizations."""
    tfidf_visualizations = [
        {'file': '01_tfidf_matrix.png', 'title': 'TF-IDF Matrix', 'description': 'Document-Term matrix with TF-IDF scores'},
        {'file': '02_idf_distribution.png', 'title': 'IDF Distribution', 'description': 'Word importance based on rarity'},
        {'file': '03_tfidf_similarities.png', 'title': 'Document Similarities', 'description': 'Comparing documents using TF-IDF'},
        {'file': '04_sgns_vs_tfidf_comparison.png', 'title': 'Method Comparison', 'description': 'TF-IDF vs SGNS overview'},
    ]
    sgns_visualizations = [
        {'file': '05_context_window.png', 'title': 'Context Window', 'description': 'How the sliding window captures relationships'},
        {'file': '06_sampling_process.png', 'title': 'Sampling Process', 'description': 'Positive and negative sampling'},
        {'file': '07_embeddings_2d.png', 'title': 'Embeddings 2D', 'description': 'Word embeddings visualized in 2D space'},
        {'file': '08_similarity_heatmap.png', 'title': 'Similarity Heatmap', 'description': 'Word-to-word similarity matrix'},
        {'file': '09_algorithm_steps.png', 'title': 'Algorithm Steps', 'description': 'Step-by-step SGNS process'},
        {'file': '10_training_dynamics.png', 'title': 'Training Dynamics', 'description': 'How embeddings improve over epochs'},
        {'file': '11_infographic_sgns.png', 'title': 'SGNS Infographic', 'description': 'Complete SGNS overview'},
    ]
    return render_template('visualizations.html', 
                         tfidf_visualizations=tfidf_visualizations,
                         sgns_visualizations=sgns_visualizations)

@app.route('/visualization/<filename>')
def view_visualization(filename):
    """View individual visualization."""
    return send_from_directory('../static/visualizations', filename)

# ============================================================================
# ROUTE: Code Examples
# ============================================================================

@app.route('/examples')
def examples_list():
    """List all interactive examples."""
    examples = [
        {'id': 1, 'title': 'Basic SGNS Usage', 'category': 'SGNS', 'difficulty': 'Beginner', 'description': 'Learn how to use SGNS from scratch'},
        {'id': 2, 'title': 'Hyperparameter Impact', 'category': 'SGNS', 'difficulty': 'Intermediate', 'description': 'See how different parameters affect learning'},
        {'id': 3, 'title': 'Context Window Effect', 'category': 'SGNS', 'difficulty': 'Intermediate', 'description': 'How window size changes word relationships'},
        {'id': 4, 'title': 'Corpus Domain Effect', 'category': 'SGNS', 'difficulty': 'Advanced', 'description': 'Different texts, different embeddings'},
        {'id': 5, 'title': 'Embedding Inspection', 'category': 'SGNS', 'difficulty': 'Advanced', 'description': 'Analyze learned embeddings'},
        {'id': 6, 'title': 'Math Behind Training', 'category': 'SGNS', 'difficulty': 'Advanced', 'description': 'The math and calculus involved'},
        {'id': 7, 'title': 'Why Negative Sampling is Fast', 'category': 'SGNS', 'difficulty': 'Intermediate', 'description': 'Understand the efficiency trick'},
        {'id': 8, 'title': 'TF-IDF Basics', 'category': 'TF-IDF', 'difficulty': 'Beginner', 'description': 'Get started with TF-IDF'},
        {'id': 9, 'title': 'SGNS vs TF-IDF', 'category': 'Comparison', 'difficulty': 'Intermediate', 'description': 'Side-by-side method comparison'},
    ]
    return render_template('examples.html', examples=examples)

@app.route('/test-capture')
def test_capture():
    """Test if output capture is working at all."""
    import sys
    import io
    
    # Test 1: Simple capture
    buffer = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer
    print("TEST MESSAGE FROM CAPTURE")
    sys.stdout = old_stdout
    captured = buffer.getvalue()
    
    return f"""
    <h1>Capture Test</h1>
    <p>Captured: '{captured}'</p>
    <p>Length: {len(captured)}</p>
    <p>Success: {len(captured) > 0}</p>
    """

@app.route('/examples/<int:example_id>')
def view_example(example_id):
    """View specific example with code and output."""
    # Get example metadata with detailed explanations
    examples = [
        {
            'id': 1,
            'title': 'Basic SGNS Usage',
            'category': 'SGNS',
            'difficulty': 'Beginner',
            'description': 'Learn how to use SGNS from scratch',
            'explanation': '''
<h4>What is this code doing?</h4>
<p>This example demonstrates the basic workflow of training a Skip-gram with Negative Sampling (SGNS) model from scratch:</p>
<ol>
    <li><strong>Building a vocabulary:</strong> The model learns which words exist in the corpus</li>
    <li><strong>Training:</strong> For each word, the model learns embeddings by predicting context words</li>
    <li><strong>Finding similarities:</strong> Once trained, we can find semantically similar words using cosine similarity</li>
</ol>
<h4>What are the results?</h4>
<p>The output shows word pairs that are semantically similar according to the learned embeddings. For example, "cat" should be similar to "dog" because they appear in similar contexts ("sat on" the mat/floor).</p>
<h4>The intuition</h4>
<p>SGNS learns word meanings by the principle: <em>"A word is known by the company it keeps"</em>. Words that appear in similar contexts will have similar embeddings. The model doesn't need explicit labels—it learns from the raw text structure.</p>
            '''
        },
        {
            'id': 2,
            'title': 'Hyperparameter Impact',
            'category': 'SGNS',
            'difficulty': 'Intermediate',
            'description': 'See how different parameters affect learning',
            'explanation': '''
<h4>What is this code doing?</h4>
<p>This example trains the same model three times with different embedding dimensions (vector sizes) to show how hyperparameters affect learning:</p>
<ul>
    <li><strong>Small embeddings (10-dim):</strong> Very compressed representation, limited capacity to capture relationships</li>
    <li><strong>Medium embeddings (50-dim):</strong> Balanced between capacity and efficiency</li>
    <li><strong>Large embeddings (100-dim):</strong> Rich representation with more space to capture nuances</li>
</ul>
<h4>What are the results?</h4>
<p>Each configuration trains on the same small corpus about "king/queen/prince/princess" relationships. The output shows the most similar words to "king" and "queen" for each embedding size.</p>
<h4>The intuition</h4>
<p>Think of embedding dimensions like the "detail level" of a photograph:</p>
<ul>
    <li>Small dimensions = low resolution, crude approximations</li>
    <li>Large dimensions = high resolution, fine details</li>
</ul>
<p>But there's a trade-off: more dimensions mean the model needs more training data to learn meaningful patterns. With a tiny corpus, even 100 dimensions might not capture relationships well. Notice how on this small dataset, all three dimensions might perform similarly!</p>
            '''
        },
        {
            'id': 3,
            'title': 'Context Window Effect',
            'category': 'SGNS',
            'difficulty': 'Intermediate',
            'description': 'How window size changes word relationships',
            'explanation': '''
<h4>What is this code doing?</h4>
<p>This example shows how the context window size (the number of surrounding words to consider) affects which words the model learns as "related".</p>
<h4>The intuition</h4>
<p>In Skip-gram, we predict context words within a window around the target word:</p>
<ul>
    <li><strong>Small window (±2):</strong> Only nearby words are treated as context. Captures syntactic relationships (parts of speech)</li>
    <li><strong>Large window (±10):</strong> Distant words are also context. Captures broader topical relationships</li>
</ul>
            '''
        },
        {
            'id': 4,
            'title': 'Corpus Domain Effect',
            'category': 'SGNS',
            'difficulty': 'Advanced',
            'description': 'Different texts, different embeddings',
            'explanation': '''
<h4>What is this code doing?</h4>
<p>This example trains models on different text domains and compares the resulting embeddings to show how domain-specific context shapes learned meanings.</p>
<h4>The intuition</h4>
<p>Embeddings are not universal—they're learned from specific text. The same word can have different "meanings" depending on context:</p>
<ul>
    <li>In medical text, "bank" might relate to blood banks</li>
    <li>In financial text, "bank" relates to money</li>
    <li>In geography, "bank" relates to rivers</li>
</ul>
            '''
        },
        {
            'id': 5,
            'title': 'Embedding Inspection',
            'category': 'SGNS',
            'difficulty': 'Advanced',
            'description': 'Analyze learned embeddings',
            'explanation': '''
<h4>What is this code doing?</h4>
<p>This example trains a model and then inspects the actual embedding vectors to understand what the model learns at the vector level.</p>
<h4>The intuition</h4>
<p>Embeddings are just vectors of numbers. While we can't easily interpret what each dimension means, we can:</p>
<ul>
    <li>Compute distances/similarities between vectors</li>
    <li>Visualize them in 2D using techniques like t-SNE</li>
    <li>Perform arithmetic operations (king - man + woman ≈ queen)</li>
</ul>
            '''
        },
        {
            'id': 6,
            'title': 'Math Behind Training',
            'category': 'SGNS',
            'difficulty': 'Advanced',
            'description': 'The math and calculus involved',
            'explanation': '''
<h4>What is this code doing?</h4>
<p>This example shows the mathematical principles behind SGNS training: computing losses, gradients, and how they update embeddings.</p>
<h4>The intuition</h4>
<p>Training SGNS involves:</p>
<ol>
    <li><strong>Forward pass:</strong> Compute the probability that context word appears near target word</li>
    <li><strong>Loss:</strong> Measure how wrong we are</li>
    <li><strong>Backward pass:</strong> Compute gradients (directions to improve)</li>
    <li><strong>Update:</strong> Move embeddings in the right direction to reduce loss</li>
</ol>
<p>The "negative sampling" trick accelerates this by only updating a few random negative examples instead of all words.</p>
            '''
        },
        {
            'id': 7,
            'title': 'Why Negative Sampling is Fast',
            'category': 'SGNS',
            'difficulty': 'Intermediate',
            'description': 'Understand the efficiency trick',
            'explanation': '''
<h4>What is this code doing?</h4>
<p>This example demonstrates why "negative sampling" is much faster than traditional softmax-based approaches.</p>
<h4>The intuition</h4>
<p><strong>Traditional Skip-gram:</strong> For each training example, compute probability for ALL words in vocabulary (slow)</p>
<p><strong>Negative Sampling:</strong> Only compare with a few random "negative" examples + 1 positive example (fast)</p>
<p>Mathematical insight: Binary classification (is this pair related or not?) is much faster than multi-class softmax over 10,000+ words.</p>
            '''
        },
        {
            'id': 8,
            'title': 'TF-IDF Basics',
            'category': 'TF-IDF',
            'difficulty': 'Beginner',
            'description': 'Get started with TF-IDF',
            'explanation': '''
<h4>What is this code doing?</h4>
<p>This example introduces TF-IDF (Term Frequency - Inverse Document Frequency), a simpler alternative to neural embeddings.</p>
<h4>The intuition</h4>
<p>TF-IDF scores words based on:</p>
<ul>
    <li><strong>TF (Term Frequency):</strong> How often a word appears in a document</li>
    <li><strong>IDF (Inverse Document Frequency):</strong> How rare the word is across all documents</li>
</ul>
<p>The intuition: common words like "the" and "is" are less informative, while rare, specific words are more meaningful.</p>
            '''
        },
        {
            'id': 9,
            'title': 'SGNS vs TF-IDF',
            'category': 'Comparison',
            'difficulty': 'Intermediate',
            'description': 'Side-by-side method comparison',
            'explanation': '''
<h4>What is this code doing?</h4>
<p>This example trains both SGNS and TF-IDF on the same corpus and compares their strengths and weaknesses.</p>
<h4>Key differences:</h4>
<table class="table table-sm">
    <thead>
        <tr>
            <th>Aspect</th>
            <th>SGNS</th>
            <th>TF-IDF</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Learning</strong></td>
            <td>Neural network with backprop</td>
            <td>Simple statistical formula</td>
        </tr>
        <tr>
            <td><strong>Context</strong></td>
            <td>Learns word order relationships</td>
            <td>Bag of words (ignores order)</td>
        </tr>
        <tr>
            <td><strong>Speed</strong></td>
            <td>Slower training, fast inference</td>
            <td>Fast for both</td>
        </tr>
        <tr>
            <td><strong>Data needed</strong></td>
            <td>Works best with large corpora</td>
            <td>Works with small data</td>
        </tr>
    </tbody>
</table>
            '''
        },
    ]
    
    example = next((e for e in examples if e['id'] == example_id), None)
    if not example:
        return "Example not found", 404
    
    # Extract source code from classroom_examples.py
    import inspect
    import classroom_examples as ce
    
    example_funcs = {
        1: ce.example_1_basic_usage,
        2: ce.example_2_hyperparameter_impact,
        3: ce.example_3_context_window_effect,
        4: ce.example_4_corpus_effect,
        5: ce.example_5_embedding_inspection,
        6: ce.example_6_math_behind_training,
        7: ce.example_7_why_fast,
        8: ce.example_8_tfidf_basics,
        9: ce.example_9_sgns_vs_tfidf,
    }
    
    code = ""
    if example_id in example_funcs:
        try:
            code = inspect.getsource(example_funcs[example_id])
        except:
            code = "# Unable to retrieve source code"
    
    result = run_example(example_id)
    return render_template('example_detail.html', example=example, example_id=example_id, result=result, code=code)

# ============================================================================
# ROUTE: Documentation
# ============================================================================

@app.route('/docs')
def documentation_hub():
    """Documentation hub."""
    docs = [
        {'title': 'Quick Start Guide', 'file': 'START_HERE.md', 'icon': 'rocket', 'color': '#28a745', 'description': 'Get started in 5 minutes', 'lines': 150},
        {'title': 'Teaching Cheatsheet', 'file': 'TEACHING_CHEATSHEET.md', 'icon': 'list', 'color': '#0d6efd', 'description': 'Quick reference guide', 'lines': 200},
        {'title': 'Visualization Guide', 'file': 'VISUALIZATION_GUIDE.md', 'icon': 'images', 'color': '#fd7e14', 'description': 'Explain all visualizations', 'lines': 250},
        {'title': 'Teaching Order', 'file': 'TEACHING_ORDER.md', 'icon': 'graduation-cap', 'color': '#6f42c1', 'description': 'Recommended lesson sequence', 'lines': 100},
        {'title': 'One-Page Summary', 'file': 'ONE_PAGE_SUMMARY.md', 'icon': 'file-alt', 'color': '#dc3545', 'description': 'Everything on one page', 'lines': 80},
    ]
    return render_template('documentation.html', docs=docs)

@app.route('/docs/<filename>')
def view_documentation(filename):
    """View specific documentation file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        # Convert markdown to HTML-safe content
        import markdown
        html_content = markdown.markdown(content)
        return render_template('doc_viewer.html', filename=filename, title=filename.replace('.md', ''), content=html_content)
    except FileNotFoundError:
        return "Document not found", 404
    except ImportError:
        # Fallback if markdown not installed
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            return render_template('doc_viewer.html', content=content, doc_name=filename)
        except Exception as e:
            return f"Error: {str(e)}", 500


# ============================================================================
# ROUTE: Classroom Mode
# ============================================================================

@app.route('/classroom')
def classroom_mode():
    """Classroom presentation mode with fullscreen visualizations."""
    return render_template('classroom.html')

@app.route('/classroom/lesson/<lesson_type>')
def classroom_lesson(lesson_type):
    """Deliver structured classroom lesson."""
    lesson_plans = {
        'quick': {
            'title': '15-Minute Quick Overview',
            'duration': 15,
            'steps': [
                {
                    'type': 'title',
                    'title': 'Skip-gram with Negative Sampling',
                    'subtitle': 'A Quick Overview',
                    'duration': 1
                },
                {
                    'type': 'content',
                    'title': 'What is NLP?',
                    'duration': 2,
                    'points': [
                        '💬 <strong>NLP (Natural Language Processing):</strong> Teaching computers to understand human language',
                        '📊 <strong>The Core Challenge:</strong> Computers only understand numbers - words are symbols',
                        '🎯 <strong>Solution:</strong> Convert words into numbers (vectors) that preserve meaning',
                        '💡 Similar words should have similar numbers, different words should be far apart'
                    ]
                },
                {
                    'type': 'content',
                    'title': 'Traditional Approach: TF-IDF',
                    'duration': 2,
                    'points': [
                        '<strong>TF (Term Frequency):</strong> Count how many times word appears in document',
                        '<strong>IDF (Inverse Document Frequency):</strong> How rare/unique the word is across all documents',
                        '<strong>Formula:</strong> TF-IDF = TF × log(Total Docs / Docs containing word)',
                        '<strong>Problem:</strong> Ignores word order and context - "dog bites man" = "man bites dog"'
                    ]
                },
                {
                    'type': 'viz',
                    'file': '04_sgns_vs_tfidf_comparison.png',
                    'duration': 1,
                    'title': 'TF-IDF vs Modern Embeddings'
                },
                {
                    'type': 'content',
                    'title': 'The Key Insight',
                    'duration': 2,
                    'points': [
                        '💡 <strong>Distributional Hypothesis:</strong> "You shall know a word by the company it keeps"',
                        '🤝 Words that appear in similar contexts have similar meanings',
                        '📚 Example: "cat" and "dog" appear near "animal", "furry", "pet"',
                        '🧠 This is how humans learn meanings too - from surrounding context!'
                    ]
                },
                {
                    'type': 'viz',
                    'file': '05_context_window.png',
                    'duration': 1,
                    'title': 'Learning from Context Windows'
                },
                {
                    'type': 'content',
                    'title': 'Skip-gram Algorithm',
                    'duration': 2,
                    'points': [
                        '🎯 <strong>Core Idea:</strong> Given a word, predict the words around it',
                        '📖 <strong>Context Window:</strong> Look at 5-10 words on each side of target word',
                        '⚡ <strong>Speed Trick - Negative Sampling:</strong> Train on few random "wrong" words instead of all words',
                        '✅ <strong>Result:</strong> Meaningful embeddings that capture semantic relationships'
                    ]
                },
                {
                    'type': 'content',
                    'title': 'Why Negative Sampling?',
                    'duration': 1,
                    'points': [
                        '⏱️ Without it: Train on 100,000+ output nodes every iteration → Extremely slow!',
                        '⚡ With it: Train on 5-20 random negative samples → 100x faster!',
                        '📊 Speed improvement with minimal accuracy loss'
                    ]
                },
                {
                    'type': 'demo',
                    'name': 'sgns',
                    'duration': 2,
                    'title': 'Interactive Demo: Skip-gram in Action'
                },
                {
                    'type': 'content',
                    'title': 'Key Takeaways',
                    'duration': 1,
                    'points': [
                        '✓ Skip-gram learns word meanings from context automatically',
                        '✓ Embeddings capture semantic and syntactic relationships',
                        '✓ Negative sampling makes training efficient enough for real applications',
                        '✓ Foundation for modern NLP and AI systems'
                    ]
                }
            ]
        },
        'standard': {
            'title': '30-Minute Standard Lesson',
            'duration': 30,
            'steps': [
                {
                    'type': 'title',
                    'title': 'Skip-gram with Negative Sampling',
                    'subtitle': 'Understanding Modern Word Embeddings',
                    'duration': 1
                },
                {
                    'type': 'content',
                    'title': 'Learning Objectives',
                    'duration': 1,
                    'points': [
                        '1️⃣ Understand why word embeddings matter',
                        '2️⃣ Compare traditional (TF-IDF) vs modern (SGNS) approaches',
                        '3️⃣ Learn how Skip-gram works',
                        '4️⃣ See practical applications and benefits'
                    ]
                },
                {
                    'type': 'content',
                    'title': 'Problem: Representing Words',
                    'duration': 2,
                    'points': [
                        '❓ <strong>Challenge 1:</strong> How do we convert words (symbols) into numbers?',
                        '❓ <strong>Challenge 2:</strong> How do we capture what words actually <em>mean</em>?',
                        '❓ <strong>Challenge 3:</strong> How do we measure similarity between word meanings?',
                        '💡 <strong>Example:</strong> Is "king" more similar to "queen" or "computer"? Why?'
                    ]
                },
                {
                    'type': 'content',
                    'title': 'TF-IDF: Frequency-Based (1960s)',
                    'duration': 3,
                    'points': [
                        '<strong>TF (Term Frequency):</strong> How often does word appear? TF = count/total_words',
                        '<strong>IDF (Inverse Document Frequency):</strong> How rare is the word? IDF = log(total_docs/docs_with_word)',
                        '<strong>Formula:</strong> TF-IDF = TF × IDF (higher for frequent but unique words)',
                        '<strong>Intuition:</strong> Common words (the, is) get low scores, unique words get high scores',
                        '<strong>Limitation:</strong> Treats "dog bites man" same as "man bites dog" - ignores word order'
                    ]
                },
                {
                    'type': 'demo',
                    'name': 'tfidf',
                    'duration': 3,
                    'title': 'TF-IDF Demo: Try It Yourself'
                },
                {
                    'type': 'content',
                    'title': 'The Problem with Frequency-Based Methods',
                    'duration': 2,
                    'points': [
                        '❌ <strong>Context-blind:</strong> Word order doesn\'t matter - semantic meaning lost',
                        '❌ <strong>Sparse vectors:</strong> Most values are zero (wasteful storage)',
                        '❌ <strong>No semantic similarity:</strong> "good" and "excellent" have completely different vectors',
                        '❌ <strong>Scale issues:</strong> All vector dimensions have same importance'
                    ]
                },
                {
                    'type': 'content',
                    'title': 'The Distributional Hypothesis',
                    'duration': 2,
                    'points': [
                        '💡 <strong>Theory:</strong> "You shall know a word by the company it keeps"',
                        '🤝 <strong>Meaning:</strong> Words in similar contexts have similar meanings',
                        '📚 <strong>Evidence:</strong> "brilliant" and "excellent" appear in similar sentences',
                        '🧠 <strong>Learning:</strong> This is how humans learn word meanings - from surrounding context!'
                    ]
                },
                {
                    'type': 'content',
                    'title': 'Skip-gram: Context-Based Approach',
                    'duration': 3,
                    'points': [
                        '🎯 <strong>Goal:</strong> Learn embeddings where similar words have similar vectors',
                        '📖 <strong>Method:</strong> Train a neural network to predict context words from target word',
                        '🔗 <strong>Context Window:</strong> Look at surrounding words (typically 5-10 words on each side)',
                        '💡 <strong>Key:</strong> The hidden layer of the network becomes our word embeddings!',
                        '✅ <strong>Result:</strong> Dense, meaningful vectors (e.g., 300 dimensions instead of 100,000)'
                    ]
                },
                {
                    'type': 'viz',
                    'file': '05_context_window.png',
                    'duration': 2,
                    'title': 'Context Windows in Action'
                },
                {
                    'type': 'content',
                    'title': 'How Skip-gram Training Works',
                    'duration': 3,
                    'points': [
                        '<strong>Step 1:</strong> Pick a target word (e.g., "cat")',
                        '<strong>Step 2:</strong> Look at words in context window (e.g., "the", "sat", "on")',
                        '<strong>Step 3:</strong> Use neural network to predict context words from target',
                        '<strong>Step 4:</strong> Calculate loss (how wrong were our predictions?)',
                        '<strong>Step 5:</strong> Update embeddings to reduce loss (backpropagation)',
                        '<strong>Step 6:</strong> Repeat with next word in the text'
                    ]
                },
                {
                    'type': 'content',
                    'title': 'The Training Challenge',
                    'duration': 2,
                    'points': [
                        '⚠️ <strong>Problem:</strong> Vocabulary size = 100,000+ words',
                        '⚠️ <strong>Output Layer:</strong> 100,000 neurons to update every training step',
                        '⚠️ <strong>Speed:</strong> Computing 100,000 probabilities is very slow',
                        '❓ <strong>Question:</strong> How do we make this practical?'
                    ]
                },
                {
                    'type': 'content',
                    'title': 'Negative Sampling Solution',
                    'duration': 3,
                    'points': [
                        '💡 <strong>Insight:</strong> We don\'t need to update all 100,000 neurons',
                        '✅ <strong>Strategy:</strong> Update only a few "wrong" words + the 1 "right" word',
                        '<strong>Example:</strong> Instead of updating 100,000 neurons, update only 6:',
                        '&nbsp;&nbsp;✓ 1 positive example (correct context word)',
                        '&nbsp;&nbsp;✗ 5 negative examples (random non-context words)',
                        '⚡ <strong>Result:</strong> 20,000x fewer updates! 100x speed improvement with minimal accuracy loss'
                    ]
                },
                {
                    'type': 'viz',
                    'file': '06_sampling_process.png',
                    'duration': 2,
                    'title': 'Negative Sampling Strategy'
                },
                {
                    'type': 'demo',
                    'name': 'sgns',
                    'duration': 3,
                    'title': 'SGNS Demo: Experience the Algorithm'
                },
                {
                    'type': 'content',
                    'title': 'Comparing the Methods',
                    'duration': 3,
                    'points': [
                        '<strong>📊 TF-IDF Approach:</strong>',
                        '&nbsp;&nbsp;• Based on word frequency in documents',
                        '&nbsp;&nbsp;• Large vectors (size = vocabulary size)',
                        '&nbsp;&nbsp;• Ignores word order and context',
                        '&nbsp;&nbsp;• Fast but poor at capturing meaning',
                        '<strong>🧠 Skip-gram Approach:</strong>',
                        '&nbsp;&nbsp;• Based on context (distributional hypothesis)',
                        '&nbsp;&nbsp;• Dense vectors (100-300 dimensions)',
                        '&nbsp;&nbsp;• Captures semantic and syntactic relationships',
                        '&nbsp;&nbsp;• Slower training but better embeddings'
                    ]
                },
                {
                    'type': 'viz',
                    'file': '04_sgns_vs_tfidf_comparison.png',
                    'duration': 1,
                    'title': 'Method Comparison'
                },
                {
                    'type': 'content',
                    'title': 'What Skip-gram Learns',
                    'duration': 2,
                    'points': [
                        '🎯 <strong>Semantic Relationships:</strong>',
                        '&nbsp;&nbsp;• king - man + woman ≈ queen',
                        '&nbsp;&nbsp;• Paris - France + Italy ≈ Rome',
                        '&nbsp;&nbsp;• Similar meanings have similar vectors',
                        '🎯 <strong>Syntactic Relationships:</strong>',
                        '&nbsp;&nbsp;• run - runs has similar direction to play - plays',
                        '&nbsp;&nbsp;• Vector arithmetic captures grammar patterns'
                    ]
                },
                {
                    'type': 'content',
                    'title': 'Real-World Applications',
                    'duration': 2,
                    'points': [
                        '🔍 <strong>Search:</strong> Find similar documents quickly',
                        '🤖 <strong>Recommendation:</strong> Suggest related products',
                        '🎨 <strong>NLP Tasks:</strong> Text classification, sentiment analysis',
                        '🌐 <strong>Knowledge:</strong> Analogies (king - man + woman ≈ queen)'
                    ]
                },
                {
                    'type': 'content',
                    'title': 'Key Takeaways',
                    'duration': 1,
                    'points': [
                        '✓ Skip-gram learns word meaning from context',
                        '✓ Negative sampling makes training efficient',
                        '✓ Word embeddings power modern NLP systems',
                        '✓ Semantic understanding from co-occurrence patterns'
                    ]
                },
                {
                    'type': 'qa',
                    'title': 'Questions & Discussion',
                    'duration': 1
                }
            ]
        },
        'comprehensive': {
            'title': '60-Minute Comprehensive Course',
            'duration': 60,
            'steps': []
        }
    }
    
    plan = lesson_plans.get(lesson_type, lesson_plans['standard'])
    return render_template('classroom_lesson.html', plan=plan)

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/generate-visualizations', methods=['POST'])
def api_generate_visualizations():
    """API to regenerate all visualizations."""
    try:
        subprocess.run([sys.executable, 'sgns_visualization.py'], check=True, capture_output=True, cwd=os.path.dirname(__file__))
        return jsonify({'status': 'success', 'message': 'Visualizations generated successfully'})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/available-visualizations')
def api_available_visualizations():
    """Get list of available visualization files."""
    viz_files = sorted([f for f in os.listdir(os.path.join(os.path.dirname(__file__), '..', 'images')) if f.endswith('.png') and f[0].isdigit()])
    return jsonify({'visualizations': viz_files})

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def run_tfidf_demo(documents):
    """Run TF-IDF on provided documents with visualizations."""
    try:
        doc_lists = [doc.lower().split() for doc in documents]
        tfidf = TFIDF()
        tfidf.fit(doc_lists)
        
        results = []
        
        # Show computation steps
        steps = []
        steps.append("Step 1: Tokenization - Split each document into words")
        for i, doc in enumerate(documents, 1):
            steps.append(f"  Doc {i}: {len(doc_lists[i-1])} tokens - {doc_lists[i-1]}")
        
        steps.append(f"\nStep 2: Build Vocabulary - Found {len(tfidf.vocab)} unique words across all documents")
        
        steps.append("\nStep 3: Calculate TF (Term Frequency) for each document")
        steps.append("  TF = (count of term in doc) / (total terms in doc)")
        
        steps.append("\nStep 4: Calculate IDF (Inverse Document Frequency)")
        steps.append("  IDF = log(total docs / docs containing term)")
        top_idf_words = sorted(tfidf.idf.items(), key=lambda x: x[1], reverse=True)[:5]
        for word, idf_score in top_idf_words:
            steps.append(f"  '{word}': IDF = {idf_score:.3f}")
        
        steps.append("\nStep 5: TF-IDF Score = TF × IDF")
        steps.append("  Higher score = more important to that document, rarer across corpus")
        
        for i, doc_list in enumerate(doc_lists):
            vec = tfidf.transform(doc_list)
            vocab_list = sorted(tfidf.vocab.keys(), key=lambda x: tfidf.vocab[x])
            top_words = sorted(
                [(word, vec[tfidf.vocab[word]]) for word in doc_list],
                key=lambda x: x[1],
                reverse=True
            )[:5]
            results.append({
                'doc_id': i + 1,
                'top_words': [{'word': w, 'score': f'{s:.3f}'} for w, s in top_words]
            })
        
        # Generate vector embeddings visualization
        viz_data = visualize_tfidf_vectors(tfidf, documents, method='pca')
        plotly_viz = create_plotly_scatter(viz_data) if 'error' not in viz_data else None
        
        return {
            'status': 'success', 
            'results': results, 
            'steps': '\n'.join(steps),
            'visualization': plotly_viz,
            'viz_metadata': {
                'num_documents': len(documents),
                'vocab_size': len(tfidf.vocab),
                'method': 'pca'
            }
        }
    except Exception as e:
        import traceback
        return {'status': 'error', 'message': f"{str(e)}\n{traceback.format_exc()}"}

def run_sgns_demo(corpus, params):
    """Run SGNS on provided corpus with visualizations."""
    try:
        sentences = [s.lower().split() for s in corpus]
        
        embedding_dim = params.get('embedding_dim', 50)
        window_size = params.get('window_size', 2)
        negative_samples = params.get('negative_samples', 5)
        epochs = params.get('epochs', 10)
        
        model = SkipGramNegativeSampling(
            embedding_dim=embedding_dim,
            window_size=window_size,
            negative_samples=negative_samples
        )
        # Build vocabulary first, then train
        model.build_vocab(sentences)
        model.train(sentences, epochs=epochs)
        
        # Build steps explanation
        steps = []
        steps.append(f"Step 1: Preprocessing")
        steps.append(f"  • Tokenized {len(sentences)} sentences into words")
        total_tokens = sum(len(s) for s in sentences)
        steps.append(f"  • Total tokens: {total_tokens}")
        
        steps.append(f"\nStep 2: Build Vocabulary")
        steps.append(f"  • Unique words: {len(model.vocab)}")
        steps.append(f"  • Vocabulary will be used to create embeddings")
        
        steps.append(f"\nStep 3: Initialize Embeddings")
        steps.append(f"  • Embedding dimension: {embedding_dim}")
        steps.append(f"  • Each word gets a {embedding_dim}-dimensional vector")
        steps.append(f"  • Initialized randomly")
        
        steps.append(f"\nStep 4: Training with Skip-gram")
        steps.append(f"  • Context window size: ±{window_size} words")
        steps.append(f"  • Negative samples per positive: {negative_samples}")
        steps.append(f"  • Training epochs: {epochs}")
        steps.append(f"  • Total context pairs generated: ~{len(sentences) * window_size * 2 * total_tokens // len(sentences)}")
        
        steps.append(f"\nStep 5: Learning Objective")
        steps.append(f"  • For each word, predict context words within window")
        steps.append(f"  • Use negative sampling: compare 1 positive vs {negative_samples} random negatives")
        steps.append(f"  • Update embeddings via backpropagation to minimize loss")
        
        steps.append(f"\nStep 6: Results - Most Similar Words")
        steps.append(f"  • Similarity computed using cosine distance between embeddings")
        steps.append(f"  • Words with similar context have similar vectors")
        
        # Get similar words for a few sample words
        vocab_list = list(model.vocab.keys())[:5]
        similarities = {}
        for word in vocab_list:
            try:
                if word in model.vocab:
                    similar = model.most_similar(word, topn=3)
                    similarities[word] = [{'word': w, 'score': f'{s:.3f}'} for w, s in similar]
            except Exception as word_err:
                # If we can't get similarities for this word, skip it
                similarities[word] = [{'word': '(no similar words)', 'score': '0.000'}]
        
        # Generate embedding visualizations
        viz_data = visualize_sgns_embeddings(model, method='pca')
        plotly_viz = create_plotly_scatter(viz_data) if 'error' not in viz_data else None
        
        return {
            'status': 'success',
            'vocab_size': len(model.vocab),
            'training_pairs': len(sentences) * window_size * 2,
            'similarities': similarities,
            'steps': '\n'.join(steps),
            'visualization': plotly_viz,
            'viz_metadata': {
                'embedding_dim': embedding_dim,
                'vocab_size': len(model.vocab),
                'method': 'pca'
            }
        }
    except Exception as e:
        import traceback
        error_msg = f"{str(e)}\n\n{traceback.format_exc()}"
        return {'status': 'error', 'message': error_msg}

def run_example(example_id):
    """Run a specific classroom example."""
    try:
        import classroom_examples as ce
        import sys
        import io
        import os
        
        example_funcs = {
            1: ce.example_1_basic_usage,
            2: ce.example_2_hyperparameter_impact,
            3: ce.example_3_context_window_effect,
            4: ce.example_4_corpus_effect,
            5: ce.example_5_embedding_inspection,
            6: ce.example_6_math_behind_training,
            7: ce.example_7_why_fast,
            8: ce.example_8_tfidf_basics,
            9: ce.example_9_sgns_vs_tfidf,
        }
        
        if example_id not in example_funcs:
            return {'status': 'error', 'message': 'Example not found'}
        
        # Create a string buffer to capture output
        output_buffer = io.StringIO()
        
        # Save original
        old_stdout = sys.stdout
        
        try:
            # Redirect stdout
            sys.stdout = output_buffer
            
            # Run the example
            try:
                example_funcs[example_id]()
            except Exception as e:
                import traceback
                output_buffer.write(f"\nERROR: {str(e)}\n")
                output_buffer.write(traceback.format_exc())
            
        finally:
            # Restore
            sys.stdout = old_stdout
        
        # Get the captured output
        output = output_buffer.getvalue()
        
        # If empty, return test output
        if not output or len(output) == 0:
            output = f"TEST: Example {example_id} executed but produced no output. This might indicate an issue with the example function."
        
        return {'status': 'success', 'output': output}
        
    except Exception as e:
        import traceback
        return {'status': 'error', 'message': str(e), 'output': traceback.format_exc()}

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("NLP Classroom - Web Application")
    print("="*70)
    print("\nStarting Flask server...")
    print("Access the application at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
