"""Generate detailed educational PPTX presentations for 6 more NLP topics.

Topics:
  1. LLM Prompt Engineering
  2. NLP Methods Comparison
  3. Neural Networks
  4. N-gram Language Models
  5. POS Tagging & HMMs
  6. TF-IDF

All slides use white backgrounds with clean, professional styling.
Reuses slide builder helpers from generate_topic_pptx.py.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from generate_topic_pptx import (
    _new_prs, add_title_slide, add_section_slide, add_content_slide,
    add_two_column_slide, add_formula_slide, add_table_slide,
    add_key_concept_slide,
    ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_RED,
)
from pptx.dml.color import RGBColor

ACCENT_PURPLE = RGBColor(0x7B, 0x1F, 0xA2)
ACCENT_TEAL = RGBColor(0x00, 0x96, 0x88)


# ══════════════════════════════════════════════════════════════════════════
# TOPIC 1: LLM PROMPT ENGINEERING
# ══════════════════════════════════════════════════════════════════════════

def build_llm_prompt_engineering(prs):
    add_title_slide(prs, "Large Language Models\n& Prompt Engineering",
                    "From Transformer Architecture to Effective Prompting Techniques",
                    ACCENT_PURPLE)

    # ── Section 1: Introduction to LLMs ──
    add_section_slide(prs, "1. Introduction to Large Language Models", ACCENT_PURPLE)

    add_key_concept_slide(prs, "What is a Large Language Model?",
        "A Language Model predicts the probability of word sequences -- "
        "essentially answering 'What word comes next?'",
        [
            "An LLM is like an incredibly well-read student who has read billions of "
            "pages of text and learned deep patterns about language.",
            "Traditional language models (N-grams) used simple statistical patterns. "
            "Modern LLMs use neural networks with billions of parameters.",
            "Capabilities: context understanding, coherent text generation, reasoning, "
            "code writing, and complex instruction following.",
        ], ACCENT_PURPLE)

    add_table_slide(prs, "Scale Timeline: Parameter Growth",
        ["Model", "Year", "Parameters", "Key Strength"],
        [
            ["GPT-1", "2018", "117 Million", "Basic language understanding"],
            ["GPT-2", "2019", "1.5 Billion", "Coherent text generation"],
            ["GPT-3", "2020", "175 Billion", "Few-shot learning"],
            ["GPT-4", "2023", "~1.7 Trillion", "Reasoning, multimodal"],
            ["Claude 3.5", "2024", "Unknown", "Long context (200K), safety"],
            ["Llama 3", "2024", "70B-405B", "Open source, efficiency"],
        ], ACCENT_PURPLE)

    add_content_slide(prs, "Transformer Architecture", [
        "Built on the Transformer (Vaswani et al., 2017)",
        "  - Uses self-attention mechanisms",
        "  - Processes sequences in parallel",
        "  - Captures long-range dependencies",
        "",
        "Self-Attention:  Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V",
        "  - Q (queries), K (keys), V (values) are learned projections of input",
        "  - Each token can 'look at' all other tokens and weigh their importance",
        "  - Scaling factor sqrt(d_k) ensures numerical stability",
    ], ACCENT_PURPLE)

    add_content_slide(prs, "Tokenization & Temperature", [
        "Tokenization (BPE - Byte-Pair Encoding):",
        '  - LLMs process tokens (subword units), not whole words',
        '  - "unhappiness" --> ["un", "happi", "ness"]',
        "  - Balances vocabulary size with coverage",
        "",
        "Temperature Scaling:  P(x_i) = exp(z_i / T) / SUM exp(z_j / T)",
        "  - T = 0: Greedy (always pick highest probability)",
        "  - T = 1: Standard softmax distribution",
        "  - T > 1: More random, creative output",
        "  - T < 1: More focused, deterministic output",
        "",
        "Warning: LLMs can hallucinate -- generate plausible but factually incorrect text. "
        "Always verify critical information!",
    ], ACCENT_PURPLE)

    # ── Section 2: How LLMs Work ──
    add_section_slide(prs, "2. How LLMs Work: Three-Stage Training", ACCENT_PURPLE)

    add_content_slide(prs, "Stage 1: Pre-training (Learning Language)", [
        "Trained on massive text corpora (books, websites, code)",
        "Task: predict the next token (self-supervised -- no human labels needed)",
        "",
        "Loss:  L = -SUM log P(w_i | w_1, w_2, ..., w_{i-1})",
        "  - Minimize negative log-likelihood of predicting each token",
        "  - This simple objective results in rich language understanding",
    ], ACCENT_PURPLE)

    add_content_slide(prs, "Stage 2: Fine-tuning & Stage 3: RLHF", [
        "Stage 2 -- Fine-tuning (Domain Specialization):",
        "  - Pre-trained model further trained on domain-specific data",
        "  - Examples: medical texts, legal documents, instruction-response pairs",
        "  - Loss: L_FT = -SUM log P(y | x) over (input, output) pairs",
        "",
        "Stage 3 -- RLHF (Alignment with Human Preferences):",
        "  - Reinforcement Learning from Human Feedback",
        "  - Humans rank model outputs; reward model learns preferences",
        "  - LLM optimized (PPO) to maximize reward while staying close to original",
        "  - Goal: helpful, honest, and harmless responses",
    ], ACCENT_PURPLE)

    add_content_slide(prs, "Emergent Abilities & In-Context Learning", [
        "Emergent abilities (appeared suddenly at scale):",
        "  - Few-shot learning: learn new tasks from just a few examples in prompt",
        "  - Chain-of-thought reasoning: break down complex problems step-by-step",
        "  - Code generation: write functional programs in multiple languages",
        "",
        "In-Context Learning:",
        "  - LLMs can learn new tasks from examples in the prompt",
        "  - WITHOUT any weight updates (learning at inference time)",
        "  - Model recognizes patterns in the prompt and applies them",
        '  - Example: "hello --> bonjour; goodbye --> au revoir; thank you --> ?"',
    ], ACCENT_PURPLE)

    # ── Section 3: Prompt Engineering Fundamentals ──
    add_section_slide(prs, "3. Prompt Engineering Fundamentals", ACCENT_PURPLE)

    add_content_slide(prs, "Core Principles of Effective Prompting", [
        "Principle 1: Be Specific",
        '  - Bad: "Tell me about dogs."',
        '  - Good: "Explain differences between working dog breeds in terms of '
        'temperament, exercise needs, and ideal living environments. Use bullet points."',
        "",
        "Principle 2: Provide Context",
        '  - Use system prompts to set role & expertise level',
        '  - "You are an expert marine biologist with 20 years of experience..."',
        "",
        "Principle 3: Structure Your Output",
        '  - Specify format: JSON, markdown, bullet points, tables',
        "",
        "Principle 4: Use Delimiters",
        "  - Separate prompt sections with triple backticks, XML tags, or headers",
    ], ACCENT_PURPLE)

    # ── Section 4: N-shot Prompting ──
    add_section_slide(prs, "4. N-shot Prompting", ACCENT_PURPLE)

    add_table_slide(prs, "N-shot Prompting Spectrum",
        ["Method", "# Examples", "When to Use", "Pros", "Cons"],
        [
            ["Zero-shot", "0", "Simple, well-known tasks",
             "Fast, no examples needed", "May misunderstand task"],
            ["One-shot", "1", "Clear task with specific format",
             "Minimal context, quick", "May not capture full pattern"],
            ["Few-shot", "3-5", "Complex or ambiguous tasks",
             "Clear pattern, high accuracy", "Uses more tokens"],
        ], ACCENT_PURPLE)

    add_content_slide(prs, "How Few-shot Prompting Works", [
        "Few-shot prompting works because LLMs perform in-context learning:",
        "  - Attention mechanism allows model to 'look back' at examples",
        "  - Form of meta-learning: model learned HOW to learn during pre-training",
        "",
        "Best Practices:",
        "  - Diverse examples: cover different edge cases",
        "  - Consistent format: use same structure for all examples",
        "  - Order matters: recent examples have more influence (recency bias)",
        "  - Label balance: include examples from all classes",
    ], ACCENT_PURPLE)

    # ── Section 5: Chain-of-Thought ──
    add_section_slide(prs, "5. Chain-of-Thought Prompting", ACCENT_PURPLE)

    add_key_concept_slide(prs, "Chain-of-Thought (CoT)",
        'Like asking a math student to "show your work" -- intermediate reasoning '
        "steps make the model more likely to arrive at the correct answer.",
        [
            'Zero-shot CoT: Simply append "Let\'s think step by step" to any prompt '
            "-- dramatically improves reasoning with NO examples needed!",
            "",
            "Self-Consistency: Generate multiple reasoning paths, take majority vote.",
            "  answer = argmax_a SUM 1[path_i --> a]",
            "",
            "Tree of Thoughts: Explore multiple reasoning branches at each step, "
            "evaluate which paths look most promising, backtrack if needed.",
        ], ACCENT_PURPLE)

    add_table_slide(prs, "CoT Performance Improvements",
        ["Task", "Standard", "Zero-shot CoT", "Few-shot CoT", "Self-Consistency"],
        [
            ["Arithmetic", "35%", "68%", "78%", "85%"],
            ["Commonsense Reasoning", "52%", "71%", "79%", "83%"],
            ["Symbolic Reasoning", "28%", "55%", "72%", "80%"],
        ], ACCENT_PURPLE)

    # ── Section 6: Generated Knowledge Prompting ──
    add_section_slide(prs, "6. Generated Knowledge Prompting", ACCENT_PURPLE)

    add_content_slide(prs, "Generated Knowledge: Two-Step Technique", [
        "Step 1: Ask the model to generate relevant facts about a topic",
        '  Prompt: "Generate 5 important facts about penguins."',
        "",
        "Step 2: Use those facts to answer the question",
        '  Prompt: "Using these facts: [facts], answer: Is a penguin a bird?"',
        "",
        "Result: Comprehensive, well-reasoned answer with supporting evidence",
        "  vs. a brief 'Yes' without explanation",
        "",
        "P(answer | question, knowledge) > P(answer | question)",
        "",
        "When to use: Knowledge-intensive QA, fact verification, complex reasoning",
        "Comparison with RAG: Generated knowledge uses LLM itself as knowledge base; "
        "RAG retrieves from external databases",
    ], ACCENT_PURPLE)

    # ── References ──
    add_section_slide(prs, "7. References", ACCENT_PURPLE)
    add_content_slide(prs, "Key References", [
        "[1] Vaswani et al. (2017) - 'Attention Is All You Need' (NeurIPS) "
        "-- Introduced the Transformer architecture",
        "",
        "[2] Brown et al. (2020) - 'Language Models are Few-Shot Learners' (NeurIPS, GPT-3) "
        "-- Scaling to 175B enables few-shot in-context learning",
        "",
        "[3] Wei et al. (2022) - 'Chain-of-Thought Prompting Elicits Reasoning' (NeurIPS) "
        "-- Intermediate reasoning steps dramatically improve performance",
        "",
        "[4] Liu et al. (2022) - 'Generated Knowledge Prompting' (ACL) "
        "-- Generating knowledge before answering improves by 10-20%",
        "",
        "[5] Wang et al. (2023) - 'Self-Consistency Improves CoT Reasoning' (ICLR) "
        "-- Multiple reasoning paths + majority vote",
        "",
        "[6] Yao et al. (2023) - 'Tree of Thoughts' (NeurIPS) "
        "-- Extends CoT with branching exploration and backtracking",
    ], ACCENT_PURPLE)


# ══════════════════════════════════════════════════════════════════════════
# TOPIC 2: NLP METHODS COMPARISON
# ══════════════════════════════════════════════════════════════════════════

def build_methods_comparison(prs):
    add_title_slide(prs, "NLP Methods:\nSide-by-Side Comparison",
                    "One Dataset, Five Methods, Different Insights\n"
                    "TF-IDF vs. Word2Vec (SGNS) vs. CBOW vs. GloVe",
                    ACCENT_TEAL)

    # ── Section 1: The Dataset ──
    add_section_slide(prs, "1. The Dataset", ACCENT_TEAL)

    add_content_slide(prs, "Shared Corpus: 8 Documents", [
        "D1: The cat sat on the mat. The cat was happy.",
        "D2: The dog ran in the park. The dog was excited.",
        "D3: A cat and a dog played together. They were happy.",
        "D4: The bird flew over the tree. The bird sang beautifully.",
        "D5: Birds and cats are animals. Dogs are animals too.",
        "D6: The mat was soft. The cat loved the mat.",
        "D7: The park was beautiful. The dog ran in the park again.",
        "D8: Animals need food and water. Cats and dogs need care.",
    ], ACCENT_TEAL)

    add_table_slide(prs, "Corpus Statistics",
        ["Statistic", "Value"],
        [
            ["Total documents", "8"],
            ["Total words (tokens)", "89"],
            ["Unique words (vocabulary)", "36"],
            ["Most frequent word", '"the" (19 times)'],
            ["Key target words", "cat (6), dog (5), bird (3), animals (3)"],
        ], ACCENT_TEAL)

    # ── Section 2: Why Learn These in 2025? ──
    add_section_slide(prs, "2. Why Learn These Methods?", ACCENT_TEAL)

    add_two_column_slide(prs, "Why These Methods Still Matter",
        "Foundational Knowledge",
        [
            "Embeddings --> Transformer embeddings",
            "Context windows --> Attention mechanisms",
            "Similarity metrics --> Dot-product attention",
            "",
            "You can't understand BERT without Word2Vec!",
            "",
            "Practical Applications:",
            "Fast, lightweight solutions",
            "Limited compute (edge devices)",
            "Search/retrieval systems",
            "TF-IDF powers search in millions of apps today",
        ],
        "Understanding Tradeoffs",
        [
            "Cost: GPT-4 API vs. local Word2Vec",
            "Interpretability: Sparse TF-IDF vs. black box",
            "Latency: Milliseconds vs. seconds",
            "Privacy: On-device vs. cloud-based",
            "",
            "Not every problem needs a $200M model!",
            "",
            "Modern RAG Systems use all three:",
            "1. TF-IDF/BM25 -- fast retrieval (ms)",
            "2. Dense embeddings -- semantic reranking",
            "3. LLM -- final answer generation",
        ])

    # ── Section 3: Method 1 - TF-IDF ──
    add_section_slide(prs, "3. Method 1: TF-IDF", ACCENT_TEAL)

    add_content_slide(prs, "TF-IDF on the Corpus", [
        "Goal: Identify important words per document by weighing frequency vs. rarity",
        "",
        "Document 1: 'The cat sat on the mat. The cat was happy.'",
        "  TF(cat) = 2/10 = 0.200,  IDF(cat) = log(8/4) = 0.693",
        "  TF-IDF(cat) = 0.139",
        "  TF(the) = 3/10 = 0.300,  IDF(the) = log(8/8) = 0.000",
        "  TF-IDF(the) = 0.000  ('the' appears everywhere -- not discriminative)",
        "",
        "Insight: No semantic meaning. Doesn't know 'cat' and 'dog' are similar.",
        "Use case: Document search, keyword extraction.",
    ], ACCENT_TEAL)

    # ── Section 4: Methods 2-4 ──
    add_section_slide(prs, "4. Methods 2-4: SGNS, CBOW, GloVe", ACCENT_TEAL)

    add_table_slide(prs, "Learned Embeddings (Simplified 3D)",
        ["Word", "SGNS Vector", "CBOW Vector", "GloVe Vector"],
        [
            ["cat", "[0.82, -0.31, 0.47]", "[0.84, -0.29, 0.46]",
             "[0.85, -0.30, 0.43]"],
            ["dog", "[0.79, -0.28, 0.54]", "[0.81, -0.26, 0.53]",
             "[0.83, -0.27, 0.49]"],
            ["bird", "[0.71, -0.22, 0.66]", "[0.73, -0.20, 0.65]",
             "[0.76, -0.21, 0.61]"],
            ["mat", "[-0.15, 0.91, -0.39]", "--", "[-0.14, 0.93, -0.34]"],
            ["park", "[-0.12, 0.88, -0.46]", "--", "[-0.11, 0.90, -0.42]"],
        ], ACCENT_TEAL)

    add_table_slide(prs, "Cosine Similarity: SGNS Results",
        ["Word Pair", "Cosine Similarity", "Interpretation"],
        [
            ["cat <-> dog", "0.92", "Very similar (both animals)"],
            ["cat <-> bird", "0.87", "Similar (both animals)"],
            ["dog <-> bird", "0.90", "Similar (both animals)"],
            ["mat <-> park", "0.98", "Very similar (both locations)"],
            ["cat <-> mat", "0.12", "Dissimilar (different groups)"],
        ], ACCENT_TEAL)

    # ── Section 5: Final Comparison ──
    add_section_slide(prs, "5. Final Comparison", ACCENT_TEAL)

    add_table_slide(prs, 'Similarity Scores for "cat" Across All Methods',
        ["Target", "TF-IDF", "SGNS", "CBOW", "GloVe"],
        [
            ["dog", "0.15", "0.92", "0.91", "0.93"],
            ["bird", "0.08", "0.87", "0.88", "0.86"],
            ["mat", "0.82 (wrong!)", "0.12", "0.14", "0.11"],
            ["park", "0.00", "0.05", "0.07", "0.04"],
            ["happy", "0.45", "0.34", "0.36", "0.38"],
        ], ACCENT_TEAL)

    add_table_slide(prs, "Method Comparison Summary",
        ["Method", "Representation", "Semantic?", "Best Use Case"],
        [
            ["TF-IDF", "Sparse (vocab size)", "None (frequency only)",
             "Document search, keywords"],
            ["SGNS", "Dense (50-300D)", "Strong (context-based)",
             "Rare words, semantic similarity"],
            ["CBOW", "Dense (50-300D)", "Strong (context-based)",
             "Frequent words, fast training"],
            ["GloVe", "Dense (50-300D)", "Strongest (global stats)",
             "Word analogies, reproducibility"],
        ], ACCENT_TEAL)

    add_two_column_slide(prs, "When to Use Which Method?",
        "Simpler Methods",
        [
            "TF-IDF:",
            "Quick document similarity",
            "No ML infrastructure needed",
            "Small datasets, interpretability",
            "",
            "CBOW:",
            "When training speed matters",
            "Vocabulary dominated by common words",
            "Online/streaming scenarios",
        ],
        "More Capable Methods",
        [
            "SGNS (Skip-gram):",
            "General-purpose embeddings",
            "Vocabulary has many rare words",
            "",
            "GloVe:",
            "Reproducible embeddings needed",
            "Have RAM for co-occurrence matrix",
            "",
            "Modern (BERT, GPT):",
            "Best results, heavier compute",
        ])


# ══════════════════════════════════════════════════════════════════════════
# TOPIC 3: NEURAL NETWORKS
# ══════════════════════════════════════════════════════════════════════════

def build_neural_networks(prs):
    add_title_slide(prs, "Neural Networks",
                    "From Single Neurons to Deep Learning\n"
                    "The Foundation of Modern AI",
                    ACCENT_BLUE)

    # ── Section 1: Intuition ──
    add_section_slide(prs, "1. What Are Neural Networks?", ACCENT_BLUE)

    add_key_concept_slide(prs, "The Voting Machine Analogy",
        "A neuron is a small voting machine: inputs get multiplied by importance "
        "weights, summed with a bias, and passed through a decision function.",
        [
            "weighted_sum = (vote_1 x weight_1) + (vote_2 x weight_2) + ... + bias",
            "If weighted_sum > threshold --> output 'YES' (1), else 'NO' (0)",
            "Weights are the key: they tell us which inputs matter more",
            "",
            "Neural networks stack layers of these units:",
            "  Early layers: detect edges and colors",
            "  Middle layers: detect shapes and parts",
            "  Final layers: recognize whole objects",
        ], ACCENT_BLUE)

    add_table_slide(prs, "Vocabulary Cheat Sheet",
        ["Term", "Meaning", "Analogy"],
        [
            ["Neuron (Node)", "Basic computing unit", "A small voting machine"],
            ["Weight", "Connection strength (learned)", "Importance score for each vote"],
            ["Bias", "Threshold adjustment", "Starting preference before seeing votes"],
            ["Activation", "Neuron's output", 'Final "YES" or "NO" decision'],
            ["Epoch", "One pass through all training data", "One full practice session"],
            ["Learning Rate", "Step size for weight updates",
             "How aggressively the student changes mind"],
        ], ACCENT_BLUE)

    add_content_slide(prs, "Quick Check: Single Neuron Calculation", [
        "If a neuron has inputs [1.0, 0.5], weights [0.5, 0.2], and bias 0.1:",
        "",
        "  Weighted sum = (1.0 x 0.5) + (0.5 x 0.2) + 0.1 = 0.7",
        "  After sigmoid: sigma(0.7) = 1/(1+e^{-0.7}) = 0.67",
        "  The neuron 'fires' with 67% strength",
    ], ACCENT_BLUE)

    # ── Section 2: XOR Problem ──
    add_section_slide(prs, "2. The XOR Problem: Why We Need Hidden Layers", ACCENT_BLUE)

    add_content_slide(prs, "Linear Separability and XOR", [
        "A single neuron can only learn LINEAR decision boundaries (one straight line).",
        "",
        "AND, OR problems: linearly separable -- a single neuron can solve them",
        "",
        "XOR truth table:  (0,0)->0,  (0,1)->1,  (1,0)->1,  (1,1)->0",
        "  Positive examples are diagonally opposite -- NO single line separates them!",
        "",
        "Solution: A network with HIDDEN LAYERS learns multiple decision boundaries",
        "and combines them. We need TWO lines to separate XOR data.",
        "",
        "Key Insight: Hidden layers allow networks to learn non-linear patterns!",
    ], ACCENT_BLUE)

    # ── Section 3: Activation Functions ──
    add_section_slide(prs, "3. Activation Functions", ACCENT_BLUE)

    add_content_slide(prs, "Why Non-Linearity?", [
        "Without activation functions, a deep network simplifies to ONE linear transform:",
        "  Layer 1: W1*x + b1",
        "  Layer 2: W2*(W1*x + b1) + b2  =  W*x + b  (just one layer!)",
        "",
        "Activation functions add 'kinks' and curves, allowing the network to fit "
        "complex, real-world patterns that aren't straight lines.",
    ], ACCENT_BLUE)

    add_table_slide(prs, "Activation Functions Comparison",
        ["Function", "Formula", "Range", "Best For", "Issue"],
        [
            ["Sigmoid", "1/(1+e^{-x})", "(0, 1)",
             "Output layer (probs)", "Vanishing gradient"],
            ["Tanh", "(e^x - e^{-x})/(e^x + e^{-x})", "(-1, 1)",
             "Hidden layers (zero-centered)", "Vanishing gradient"],
            ["ReLU", "max(0, x)", "[0, inf)",
             "Default hidden layer", "Dying ReLU problem"],
            ["Leaky ReLU", "max(0.01x, x)", "(-inf, inf)",
             "When ReLU neurons die", "Hyperparameter (0.01)"],
        ], ACCENT_BLUE)

    add_content_slide(prs, "When to Use Which?", [
        "Output layer:",
        "  - Binary classification (yes/no)? --> Sigmoid (outputs 0-1)",
        "  - Multi-class (which category)? --> Softmax (outputs probabilities)",
        "",
        "Hidden layers:",
        "  - Most cases? --> ReLU (fast, no vanishing gradients)",
        "  - Experiencing dying neurons? --> Leaky ReLU",
        "  - Need zero-centered outputs? --> Tanh",
    ], ACCENT_BLUE)

    # ── Section 4: Forward Propagation ──
    add_section_slide(prs, "4. Forward Propagation", ACCENT_BLUE)

    add_content_slide(prs, "Tracing a Number Through the Network", [
        "Input: x = [1.0, 0.5],  Weights W,  Bias b,  Activation sigma",
        "",
        "Step 1: Hidden Layer",
        "  z_1 = (1.0 x 0.5) + (0.5 x 0.2) + 0.1 = 0.7",
        "  a_1 = sigma(0.7) = 0.668",
        "  (repeat for all hidden neurons...)",
        "",
        "Step 2: Output Layer",
        "  z_2 = (0.668 x 0.6) + ... + 0.1 = -0.12",
        "  y_hat = sigma(-0.12) = 0.47",
        "",
        "The network predicts 47% probability for this input.",
        "Forward propagation is just repeated multiplication, addition, and activation!",
    ], ACCENT_BLUE)

    add_formula_slide(prs, "Forward Propagation Equations",
        [
            "Hidden: z[1] = W[1] . x + b[1],   a[1] = sigma(z[1])",
            "Output: z[2] = W[2] . a[1] + b[2],  y_hat = sigma(z[2])",
        ],
        [
            "x = input data;  W = weight matrices;  b = bias vectors;  "
            "sigma = activation function (e.g., sigmoid).",
            "Each layer transforms its input through weighted sum + bias + activation. "
            "The output is the network's prediction.",
        ], ACCENT_BLUE)

    # ── Section 5: Training Cycle ──
    add_section_slide(prs, "5. The Complete Training Cycle", ACCENT_BLUE)

    add_content_slide(prs, "Training: The Student & Teacher Analogy", [
        "1. Forward Pass = Student attempts problem",
        '   Uses current knowledge (weights) to make a prediction',
        "",
        "2. Compute Loss = Teacher checks answer",
        '   Compares prediction to correct answer, calculates error',
        '   Loss (BCE): L = -[y log(y_hat) + (1-y) log(1-y_hat)]',
        "",
        "3. Backward Pass (Backpropagation) = Teacher explains mistakes",
        '   Traces through reasoning to find which weights were wrong',
        '   Uses the chain rule to propagate error signals backward',
        "",
        "4. Update Weights = Student adjusts understanding",
        '   W := W - alpha * dL/dW   (gradient descent)',
        "",
        "REPEAT thousands of times --> Expert level achieved!",
    ], ACCENT_BLUE)

    add_formula_slide(prs, "Backpropagation Equations",
        [
            "Loss: L = -[y log(y_hat) + (1-y) log(1-y_hat)]",
            "Output gradient: dL/dz[2] = y_hat - y",
            "Hidden gradient: dL/dz[1] = W[2]^T (dL/dz[2]) * sigma'(z[1])",
            "Weight update: W := W - alpha * dL/dW",
        ],
        [
            "Binary cross-entropy loss: provides strong gradients for wrong predictions.",
            "Output layer error: simply prediction minus truth.",
            "Hidden layer: chain rule propagates error backward through weights.",
            "Gradient descent: move weights in direction that reduces loss. "
            "alpha = learning rate (too big = unstable, too small = slow).",
        ], ACCENT_BLUE)

    add_table_slide(prs, "Learning Rate Effects",
        ["Learning Rate", "Behavior"],
        [
            ["Too Small (0.01)", "Slow, steady progress, might get stuck"],
            ["Sweet Spot (0.1-0.3)", "Fast, stable convergence"],
            ["Too Large (0.5+)", "Overshoots, bounces around, might diverge"],
        ], ACCENT_BLUE)

    # ── Section 6: Common Misconceptions ──
    add_section_slide(prs, "6. Practical Considerations", ACCENT_BLUE)

    add_two_column_slide(prs, "Common Misconceptions vs. Truth",
        "Myths",
        [
            '"Backpropagation is complicated math we must memorize."',
            "",
            '"Training is just about making the loss smaller."',
            "",
            '"Bigger networks are always better."',
        ],
        "Truth",
        [
            "It's just the chain rule applied repeatedly. "
            "Computers calculate derivatives automatically!",
            "",
            "Training is about finding weights that GENERALIZE to new data. "
            "Too much training leads to overfitting.",
            "",
            "Bigger networks need more data. Without enough data, "
            "they memorize instead of learning.",
        ])

    # ── References ──
    add_section_slide(prs, "7. References", ACCENT_BLUE)
    add_content_slide(prs, "Key References", [
        "McCulloch & Pitts (1943) - A Logical Calculus of Ideas Immanent in "
        "Nervous Activity -- Simplified model of biological computation",
        "",
        "Rosenblatt (1958) - The Perceptron -- Formalized the neuron concept",
        "",
        "Rumelhart, Hinton & Williams (1986) - Learning representations by "
        "back-propagating errors -- Popularized backpropagation",
        "",
        "Goodfellow, Bengio & Courville (2016) - Deep Learning -- "
        "Definitive modern textbook (freely available online)",
    ], ACCENT_BLUE)


# ══════════════════════════════════════════════════════════════════════════
# TOPIC 4: N-GRAM LANGUAGE MODELS
# ══════════════════════════════════════════════════════════════════════════

def build_ngram(prs):
    add_title_slide(prs, "N-gram Language Models",
                    "Probabilistic Sequence Modeling\n"
                    "Predicting the Next Word from the Previous N-1 Words",
                    ACCENT_GREEN)

    # ── Section 1: Intuition ──
    add_section_slide(prs, "1. Intuition", ACCENT_GREEN)

    add_key_concept_slide(prs, "What is an N-gram Language Model?",
        "An N-gram model predicts the next word based on the previous N-1 words. "
        'Like your phone keyboard suggesting "going" after you type "I am".',
        [
            "The Markov Assumption: next word depends only on the last N-1 words, "
            "not the entire history.",
            "P(w_k | w_1...w_{k-1})  ~=  P(w_k | w_{k-N+1}...w_{k-1})",
            "",
            "Unigram (N=1): each word independent -- P(cat) = count(cat)/total",
            "Bigram (N=2): depends on previous 1 word -- P(meow | cat)",
            "Trigram (N=3): depends on previous 2 words -- P(loudly | cat meow)",
        ], ACCENT_GREEN)

    add_content_slide(prs, "Sentence Breakdown Example", [
        'Sentence: "The cat sat on the mat"',
        "",
        "Bigrams: <s> The, The cat, cat sat, sat on, on the, the mat, mat </s>",
        "",
        "Trigrams: <s><s> The, <s> The cat, The cat sat, cat sat on, ...",
        "",
        "Limitation: Cannot capture long-range dependencies!",
        '  "The cat that the dog chased ___" -- correct: "ran" (agreeing with "cat")',
        '  Bigram model only sees "chased ___" and might predict "the" or "away"',
    ], ACCENT_GREEN)

    # ── Section 2: Mathematics ──
    add_section_slide(prs, "2. N-gram Mathematics", ACCENT_GREEN)

    add_formula_slide(prs, "Chain Rule & N-gram Approximation",
        [
            "Chain Rule: P(w_1...w_n) = PROD_{k=1}^{n} P(w_k | w_1...w_{k-1})",
            "Bigram: P(w_k | w_1...w_{k-1})  ~=  P(w_k | w_{k-1})",
            "MLE: P(w_n | w_{n-1}) = C(w_{n-1}, w_n) / C(w_{n-1})",
        ],
        [
            "Exact but intractable for long sequences.",
            "Bigram approximation: next word depends only on immediately previous word.",
            "Maximum Likelihood Estimation: count bigram occurrences divided by "
            "context occurrences. Simple and effective!",
        ], ACCENT_GREEN)

    # ── Section 3: Worked Example ──
    add_section_slide(prs, "3. Worked Example", ACCENT_GREEN)

    add_content_slide(prs, 'Corpus: "I am Sam. Sam I am. I do not like green eggs and ham."', [
        "Sentences with boundaries:",
        "  <s> I am Sam </s>",
        "  <s> Sam I am </s>",
        "  <s> I do not like green eggs and ham </s>",
    ], ACCENT_GREEN)

    add_table_slide(prs, "Bigram Counts and Probabilities",
        ["Bigram", "Count", "Context Count", "Probability"],
        [
            ["<s> I", "2", "C(<s>)=3", "2/3 = 0.667"],
            ["<s> Sam", "1", "C(<s>)=3", "1/3 = 0.333"],
            ["I am", "2", "C(I)=3", "2/3 = 0.667"],
            ["I do", "1", "C(I)=3", "1/3 = 0.333"],
            ["am Sam", "1", "C(am)=2", "1/2 = 0.500"],
            ["am </s>", "1", "C(am)=2", "1/2 = 0.500"],
            ["Sam I", "1", "C(Sam)=2", "1/2 = 0.500"],
            ["Sam </s>", "1", "C(Sam)=2", "1/2 = 0.500"],
        ], ACCENT_GREEN)

    add_content_slide(prs, "Sentence Probability Calculation", [
        "P(<s> I am Sam </s>) using bigram model:",
        "",
        "= P(I|<s>) x P(am|I) x P(Sam|am) x P(</s>|Sam)",
        "= 2/3 x 2/3 x 1/2 x 1/2",
        "= 0.667 x 0.667 x 0.500 x 0.500",
        "= 0.111",
        "",
        "The Zero Probability Problem:",
        '  P(likes|Sam) = C("Sam likes")/C("Sam") = 0/2 = 0',
        "  The ENTIRE sentence probability becomes zero!",
        "  Solution: Smoothing techniques",
    ], ACCENT_GREEN)

    # ── Section 4: Smoothing ──
    add_section_slide(prs, "4. Smoothing Techniques", ACCENT_GREEN)

    add_formula_slide(prs, "Smoothing Methods",
        [
            "Laplace (Add-1): P(w_n|w_{n-1}) = (C(w_{n-1},w_n) + 1) / (C(w_{n-1}) + V)",
            "Add-k: P(w_n|w_{n-1}) = (C(w_{n-1},w_n) + k) / (C(w_{n-1}) + kV)",
            "Interpolation: P_hat = lambda_1 P_tri + lambda_2 P_bi + lambda_3 P_uni",
        ],
        [
            "Laplace: Add 1 to every count. Simple but distorts distribution heavily "
            "with large vocabularies.",
            "Add-k: More flexible (k=0.01 to 0.5). Less distortion than add-1. "
            "Tune k on validation set.",
            "Interpolation: Mix trigram + bigram + unigram. lambdas sum to 1, "
            "tuned on held-out set. If trigram unseen, bigram/unigram provide fallback.",
        ], ACCENT_GREEN)

    add_content_slide(prs, "Smoothing Example: P(likes | Sam)", [
        "Vocabulary V = 12",
        "",
        "Without smoothing (MLE):  P = 0/2 = 0.000",
        "",
        "Laplace (Add-1):  P = (0+1)/(2+12) = 1/14 = 0.071",
        "  Problem: P(I|Sam) drops from 0.500 to 0.143 -- too much distortion!",
        "",
        "Add-k (k=0.1):  P = (0+0.1)/(2+1.2) = 0.1/3.2 = 0.031",
        "  P(I|Sam) = 1.1/3.2 = 0.344 -- much less distortion",
        "",
        "Interpolation (lambda=[0.5, 0.3, 0.2]):",
        "  P = 0.5(0) + 0.3(P_bi) + 0.2(P_uni) = non-zero even when trigram is 0",
    ], ACCENT_GREEN)

    # ── Section 5: Backoff ──
    add_section_slide(prs, "5. Backoff Methods", ACCENT_GREEN)

    add_two_column_slide(prs, "Katz Backoff vs. Stupid Backoff",
        "Katz Backoff",
        [
            "Uses lower-order model ONLY when",
            "higher-order count is zero",
            "",
            "P* = discounted probability",
            "alpha = backoff weight",
            "(ensures probabilities sum to 1)",
            "",
            "Proper probability model",
        ],
        "Stupid Backoff",
        [
            "Simpler, non-probabilistic variant",
            "Designed for web scale (trillions of tokens)",
            "",
            "S = count/context  if seen",
            "S = 0.4 x S(lower-order)  otherwise",
            "",
            "Scores don't sum to 1",
            "But relative ranking preserved",
            "Used in Google Web 1T N-grams",
        ])

    # ── Section 6: Perplexity ──
    add_section_slide(prs, "6. Perplexity", ACCENT_GREEN)

    add_formula_slide(prs, "Perplexity: How Surprised is the Model?",
        [
            "PP(W) = P(w_1...w_N)^{-1/N}",
            "PP(W) = 2^{H(W)}   where H(W) = -(1/N) log_2 P(w_1...w_N)",
        ],
        [
            "Inverse probability normalized by sequence length. "
            "Lower perplexity = better model.",
            "Equivalent to 2 raised to the cross-entropy. "
            "Interpretation: average number of equally likely next-word choices.",
        ], ACCENT_GREEN)

    add_table_slide(prs, "Typical Perplexity Values",
        ["Model", "Perplexity", "Interpretation"],
        [
            ["Perfect model", "1", "Knows exactly what comes next"],
            ["Good N-gram model", "50-200", "Typical for English text"],
            ["Random guessing", "V (e.g., 50,000)", "Uniform over vocabulary"],
            ["Neural LMs (2015)", "50-80", "Significant improvement"],
            ["Modern transformers", "< 20", "State of the art"],
        ], ACCENT_GREEN)

    add_content_slide(prs, "Perplexity Calculation Example", [
        'P("I am Sam") = 0.111,  N = 3 words',
        "",
        "PP = (0.111)^{-1/3} = (1/0.111)^{1/3} = (9.009)^{0.333} = 2.08",
        "",
        "Interpretation: On average, the model has about 2 equally likely choices "
        "at each word position.",
    ], ACCENT_GREEN)

    # ── References ──
    add_section_slide(prs, "7. References", ACCENT_GREEN)
    add_content_slide(prs, "Key References", [
        "[1] Jurafsky & Martin (2024) - Speech and Language Processing, Ch. 3 "
        "-- Definitive textbook on N-gram models",
        "",
        "[2] Shannon (1951) - 'Prediction and Entropy of Printed English' "
        "-- Introduced perplexity; English has ~1-1.5 bits/char entropy",
        "",
        "[3] Chen & Goodman (1999) - 'An Empirical Study of Smoothing Techniques' "
        "-- Comprehensive comparison; Kneser-Ney performs best",
        "",
        "[4] Brants et al. (2007) - 'Large Language Models in Machine Translation' "
        "-- Introduced Stupid Backoff; Google Web 1T 5-gram corpus",
    ], ACCENT_GREEN)


# ══════════════════════════════════════════════════════════════════════════
# TOPIC 5: POS TAGGING & HMMs
# ══════════════════════════════════════════════════════════════════════════

def build_pos_tagging(prs):
    add_title_slide(prs, "POS Tagging, Markov Chains\n& Hidden Markov Models",
                    "Sequence Labeling for Parts of Speech\n"
                    "From Observable Chains to Hidden State Inference",
                    ACCENT_ORANGE)

    # ── Section 1: Intuition ──
    add_section_slide(prs, "1. What is POS Tagging?", ACCENT_ORANGE)

    add_content_slide(prs, "Part-of-Speech Tagging", [
        "Assigning a grammatical category to each word in a sentence.",
        "The oldest and most fundamental task in NLP.",
        "",
        '"The cat sat on the mat"',
        "  The -> DT (Determiner)",
        "  cat -> NN (Noun)",
        "  sat -> VBD (Verb, past tense)",
        "  on  -> IN (Preposition)",
        "  the -> DT (Determiner)",
        "  mat -> NN (Noun)",
    ], ACCENT_ORANGE)

    add_content_slide(prs, "Why POS Tagging Matters & The Ambiguity Problem", [
        "Applications: parsing, NER, information retrieval, machine translation, "
        "text-to-speech (pronunciation depends on POS)",
        "",
        "The Core Challenge: Lexical Ambiguity",
        '  "book" --> Noun: "I read a book" vs. Verb: "Please book the flight"',
        '  "can"  --> Modal: "I can swim" vs. Noun: "Open the can"',
        '  "run"  --> Verb: "I run daily" vs. Noun: "a run in the park"',
        "",
        'Try it: "The fish can swim"',
        "  Three out of four content words are ambiguous!",
        "  Context resolves ambiguity -- POS taggers use neighboring tags.",
    ], ACCENT_ORANGE)

    # ── Section 2: Word Classes ──
    add_section_slide(prs, "2. Word Classes", ACCENT_ORANGE)

    add_two_column_slide(prs, "Open vs. Closed Word Classes",
        "Open Classes (new words added regularly)",
        [
            "Nouns (NN): dog, city, freedom, blockchain",
            "Verbs (VB): run, think, optimize",
            "Adjectives (JJ): big, red, computational",
            "Adverbs (RB): quickly, very, efficiently",
            "",
            "Productive -- new words coined regularly",
        ],
        "Closed Classes (fixed membership)",
        [
            "Determiners (DT): the, a, this, every",
            "Pronouns (PRP): I, you, he, she, it",
            "Prepositions (IN): in, on, at, by, with",
            "Conjunctions (CC): and, but, or",
            "Modals (MD): can, could, will, should",
            "",
            "Rarely add new members",
        ])

    # ── Section 3: Penn Treebank ──
    add_section_slide(prs, "3. The Penn Treebank Tagset (45 tags)", ACCENT_ORANGE)

    add_table_slide(prs, "Key Penn Treebank Tags (Subset)",
        ["Tag", "Description", "Example"],
        [
            ["DT", "Determiner", "the, a, these"],
            ["NN / NNS", "Noun singular / plural", "dog / dogs"],
            ["NNP", "Proper noun", "London, Mary"],
            ["VB / VBD", "Verb base / past", "run / ran"],
            ["VBG / VBN", "Gerund / past participle", "running / run"],
            ["VBZ", "Verb 3rd person singular", "runs"],
            ["JJ / JJR / JJS", "Adjective / comparative / superlative",
             "big / bigger / biggest"],
            ["RB", "Adverb", "quickly, never"],
            ["IN", "Preposition / subord. conj.", "in, of, that"],
            ["CC", "Coordinating conjunction", "and, but, or"],
            ["MD", "Modal", "can, will, might"],
            ["PRP", "Personal pronoun", "I, he, she"],
        ], ACCENT_ORANGE)

    # ── Section 4: Markov Chains ──
    add_section_slide(prs, "4. Markov Chains", ACCENT_ORANGE)

    add_formula_slide(prs, "Markov Chain: States & Transitions",
        [
            "Markov Property: P(q_t | q_1,...,q_{t-1}) = P(q_t | q_{t-1})",
            "Transition: a_ij = P(q_t = s_j | q_{t-1} = s_i),  SUM_j a_ij = 1",
            "Sequence: P(q_1,...,q_T) = pi_{q1} * PROD_{t=2}^{T} a_{q_{t-1},q_t}",
        ],
        [
            "The future depends only on the present, not the entire history.",
            "Each row of the transition matrix sums to 1 (must go somewhere).",
            "Probability of entire sequence = initial probability x product of transitions.",
        ], ACCENT_ORANGE)

    add_content_slide(prs, "Example: Weather Markov Chain", [
        "Transition matrix:",
        "  Sunny -> Sunny: 0.7,  Sunny -> Rainy: 0.3",
        "  Rainy -> Sunny: 0.4,  Rainy -> Rainy: 0.6",
        "",
        "P(Sunny, Rainy, Rainy) = pi(Sunny) x a(S->R) x a(R->R)",
        "                       = 0.6 x 0.3 x 0.6 = 0.108",
        "",
        "Key Insight: Markov chains model OBSERVABLE sequences.",
        "In POS tagging, we observe WORDS but want to infer TAGS.",
        "Tags are hidden --> we need Hidden Markov Models!",
    ], ACCENT_ORANGE)

    # ── Section 5: HMMs ──
    add_section_slide(prs, "5. Hidden Markov Models", ACCENT_ORANGE)

    add_key_concept_slide(prs, "HMM: Hidden States + Observations",
        "In an HMM, states are not directly observable. Each state produces an "
        "observation (emission) according to a probability distribution.",
        [
            "HMM Components: lambda = (A, B, pi)",
            "  A = Transition matrix: a_ij = P(q_t=j | q_{t-1}=i)",
            "  B = Emission matrix: b_j(o_t) = P(o_t | q_t=j)",
            "  pi = Initial state distribution",
            "",
            "Three Fundamental Problems:",
            "  1. Evaluation: P(O|lambda) --> Forward algorithm",
            "  2. Decoding: best state sequence --> Viterbi algorithm",
            "  3. Learning: find best parameters --> Baum-Welch (EM)",
        ], ACCENT_ORANGE)

    add_content_slide(prs, "HMM for POS Tagging", [
        "Mapping:",
        "  Hidden states = POS tags (NN, VB, DT, JJ, ...)",
        "  Observations = Words in the sentence",
        "  Transition A: How likely is tag t_j after tag t_i?",
        "  Emission B: How likely is word w given tag t?",
        "",
        "Goal: T* = argmax_T P(T|W) = argmax_T P(W|T) . P(T)",
        "",
        "Training (MLE from tagged corpora):",
        "  P(t_i | t_{i-1}) = C(t_{i-1}, t_i) / C(t_{i-1})",
        "  P(w_i | t_i) = C(t_i, w_i) / C(t_i)",
    ], ACCENT_ORANGE)

    # ── Section 6: Viterbi ──
    add_section_slide(prs, "6. The Viterbi Algorithm", ACCENT_ORANGE)

    add_formula_slide(prs, "Viterbi: Dynamic Programming for Decoding",
        [
            "Init: v_1(j) = pi_j * b_j(o_1)",
            "Recursion: v_t(j) = max_i [v_{t-1}(i) * a_ij * b_j(o_t)]",
            "Backpointer: bp_t(j) = argmax_i [v_{t-1}(i) * a_ij * b_j(o_t)]",
        ],
        [
            "For each state j, initial Viterbi value = initial prob x emission prob.",
            "At each step, find best previous state i that maximizes path probability.",
            "Backpointers record which state gave the max, enabling backtrace.",
        ], ACCENT_ORANGE)

    add_content_slide(prs, 'Worked Example: Viterbi on "I saw the dog"', [
        "Initialization (word = 'I'):",
        "  v_1(PRP) = 0.40 x 0.50 = 0.200  (highest!)",
        "  v_1(VBD) = 0.05 x 0.01 = 0.0005",
        "  v_1(DT)  = 0.30 x 0.01 = 0.003",
        "  v_1(NN)  = 0.25 x 0.01 = 0.0025",
        "",
        "Recursion (word = 'saw'):",
        "  v_2(VBD) = max[0.200 x 0.50 x 0.40, ...] = 0.040 (from PRP)",
        "",
        "Recursion (word = 'the'): v_3(DT) = 0.016 (from VBD)",
        "Recursion (word = 'dog'): v_4(NN) = 0.00776 (from DT)",
        "",
        "Backtrace: PRP -> VBD -> DT -> NN",
        "Result: I/PRP  saw/VBD  the/DT  dog/NN",
    ], ACCENT_ORANGE)

    # ── References ──
    add_section_slide(prs, "7. References", ACCENT_ORANGE)
    add_content_slide(prs, "Key References", [
        "[1] Jurafsky & Martin (2024) - Speech and Language Processing, Ch. 8 "
        "-- Sequence Labeling for POS and Named Entities",
        "",
        "[2] Marcus, Santorini & Marcinkiewicz (1993) - 'Building a Large Annotated "
        "Corpus of English: The Penn Treebank' -- Defined the 45-tag standard",
        "",
        "[3] Rabiner (1989) - 'A Tutorial on Hidden Markov Models' "
        "-- Classic tutorial on HMMs and their applications",
        "",
        "[4] Manning & Schutze (1999) - Foundations of Statistical NLP, Ch. 10 "
        "-- POS Tagging algorithms and evaluation",
    ], ACCENT_ORANGE)


# ══════════════════════════════════════════════════════════════════════════
# TOPIC 6: TF-IDF
# ══════════════════════════════════════════════════════════════════════════

def build_tfidf(prs):
    add_title_slide(prs, "TF-IDF\nTerm Frequency - Inverse Document Frequency",
                    "Statistical Approach to Text Representation\n"
                    "The Foundation of Information Retrieval",
                    ACCENT_RED)

    # ── Section 1: Intuition ──
    add_section_slide(prs, "1. Intuition", ACCENT_RED)

    add_key_concept_slide(prs, "What is TF-IDF?",
        "Words that appear frequently in a specific document but rarely across "
        "all documents are likely the most important for understanding that document.",
        [
            "TF-IDF = Term Frequency x Inverse Document Frequency",
            "A numerical statistic reflecting how important a word is to a document "
            "within a collection (corpus).",
            "",
            "Historical context: Concept introduced by Karen Sparck Jones (1972); "
            "refined by Salton & Buckley (1988).",
        ], ACCENT_RED)

    add_content_slide(prs, "The Library Analogy", [
        'A librarian looking for books about "marine biology":',
        "",
        'Common words ("the", "is", "and") appear in EVERY book',
        "  --> Don't help identify what a book is about",
        "",
        'Rare but relevant words ("coral", "plankton", "cetacean")',
        "  --> Appear frequently in marine biology books but rarely in cookbooks",
        "  --> These are the discriminative keywords!",
        "",
        "TF-IDF captures exactly this intuition mathematically.",
    ], ACCENT_RED)

    add_two_column_slide(prs, "The Two Components",
        "Term Frequency (TF)",
        [
            '"How often does this word appear HERE?"',
            "",
            "TF = count(word) / total_words",
            "",
            "If a recipe mentions 'chocolate' 15 times,",
            "it's probably about chocolate.",
            "",
            "Higher frequency in this doc = higher TF",
        ],
        "Inverse Document Frequency (IDF)",
        [
            '"How SPECIAL is this word?"',
            "",
            "IDF = log(total_docs / docs_with_word)",
            "",
            '"the" appears everywhere (IDF ~ 0)',
            '"quantum" appears in few docs (IDF high)',
            "",
            "Rarity across corpus = Importance",
        ])

    # ── Section 2: Simple Example ──
    add_section_slide(prs, "2. Simple Numerical Example", ACCENT_RED)

    add_content_slide(prs, 'Tiny Corpus: 2 Documents, 2 Words', [
        'Document 1: "cat cat dog"',
        'Document 2: "dog dog dog"',
        "",
        "Counts: cat -> Doc1: 2, Doc2: 0 (appears in 1 doc)",
        "        dog -> Doc1: 1, Doc2: 3 (appears in 2 docs)",
    ], ACCENT_RED)

    add_table_slide(prs, "Step-by-Step Calculation",
        ["Step", "cat (Doc 1)", "dog (Doc 1)", "cat (Doc 2)", "dog (Doc 2)"],
        [
            ["TF", "2/3 = 0.667", "1/3 = 0.333", "0/3 = 0.000", "3/3 = 1.000"],
            ["IDF", "log(2/1)=0.301", "log(2/2)=0.000",
             "log(2/1)=0.301", "log(2/2)=0.000"],
            ["TF-IDF", "0.667x0.301=0.201", "0.333x0.000=0.000",
             "0.000x0.301=0.000", "1.000x0.000=0.000"],
        ], ACCENT_RED)

    add_content_slide(prs, "Key Insight from the Example", [
        '"cat" has the ONLY non-zero TF-IDF score (0.201) in Document 1!',
        "",
        "Why?",
        '  - "cat" appears frequently in Doc 1 (high TF) AND only in Doc 1 (high IDF)',
        '  - "dog" appears in BOTH documents, so IDF = 0 --> ALL its TF-IDF scores = 0',
        "",
        "Conclusion: TF-IDF perfectly identifies what makes Document 1 unique -- "
        "it's the one about cats!",
    ], ACCENT_RED)

    # ── Section 3: Worked Example ──
    add_section_slide(prs, "3. Three-Document Worked Example", ACCENT_RED)

    add_content_slide(prs, "The Corpus", [
        'Document 1: "The cat sat on the mat"',
        'Document 2: "The dog sat on the log"',
        'Document 3: "The cat chased the dog"',
    ], ACCENT_RED)

    add_table_slide(prs, "IDF Values",
        ["Word", "Docs Containing", "IDF = log(3/n)", "Interpretation"],
        [
            ["the", "3", "log(3/3) = 0.000", "Appears everywhere -- not useful"],
            ["cat", "2", "log(3/2) = 0.176", "Somewhat distinctive"],
            ["sat", "2", "log(3/2) = 0.176", "Somewhat distinctive"],
            ["dog", "2", "log(3/2) = 0.176", "Somewhat distinctive"],
            ["mat", "1", "log(3/1) = 0.477", "Very distinctive!"],
            ["chased", "1", "log(3/1) = 0.477", "Very distinctive!"],
        ], ACCENT_RED)

    add_table_slide(prs, "Final TF-IDF Scores",
        ["Word", "Doc 1", "Doc 2", "Doc 3"],
        [
            ["the", "0.000", "0.000", "0.000"],
            ["cat", "0.029", "0.000", "0.035"],
            ["mat", "0.080", "0.000", "0.000"],
            ["chased", "0.000", "0.000", "0.095"],
            ["dog", "0.000", "0.029", "0.035"],
            ["log", "0.000", "0.080", "0.000"],
        ], ACCENT_RED)

    add_content_slide(prs, "Interpretation", [
        'Document 1\'s most important word: "mat" (0.080) -- unique to this doc!',
        'Document 2\'s most important word: "log" (0.080) -- unique to this doc!',
        'Document 3\'s most important word: "chased" (0.095) -- unique to this doc!',
        '"the" scores 0 everywhere -- it doesn\'t help distinguish any document.',
    ], ACCENT_RED)

    # ── Section 4: Mathematical Foundations ──
    add_section_slide(prs, "4. Mathematical Foundations", ACCENT_RED)

    add_formula_slide(prs, "The Complete TF-IDF Formula",
        [
            "TF(t, d) = f_{t,d} / SUM_{t'} f_{t',d}",
            "IDF(t, D) = log(N / |{d in D : t in d}|)",
            "TF-IDF(t, d, D) = TF(t, d) x IDF(t, D)",
        ],
        [
            "TF: Raw count of term t in doc d, normalized by total terms in d. "
            "Prevents bias toward longer documents.",
            "IDF: Log of total documents N divided by documents containing t. "
            "Log dampens extreme differences; connects to information theory.",
            "Combined: high when term is frequent here AND rare across corpus.",
        ], ACCENT_RED)

    add_table_slide(prs, "TF-IDF Score Interpretation",
        ["Scenario", "TF", "IDF", "TF-IDF", "Meaning"],
        [
            ["Often here, rare in corpus", "High", "High", "HIGH", "Very important"],
            ["Often here, common in corpus", "High", "Low", "Medium",
             "Frequent but not distinctive"],
            ["Rare here, rare in corpus", "Low", "High", "Medium",
             "Distinctive but not emphasized"],
            ["Rare here, common in corpus", "Low", "Low", "LOW", "Not important"],
            ["Doesn't appear here", "0", "Any", "0", "Not relevant"],
        ], ACCENT_RED)

    add_formula_slide(prs, "Smoothed IDF (Edge Case: Division by Zero)",
        [
            "IDF(t) = log((N + 1) / (1 + |{d in D : t in d}|))",
        ],
        [
            "If a term doesn't appear in any document, standard IDF divides by zero. "
            "Adding 1 to numerator and denominator prevents this edge case.",
        ], ACCENT_RED)

    # ── Section 5: Variants ──
    add_section_slide(prs, "5. TF-IDF Variants & When to Use", ACCENT_RED)

    add_table_slide(prs, "Common TF-IDF Variants",
        ["Variant", "Formula", "Benefit"],
        [
            ["Log-Normalized TF", "1 + log(f_{t,d})",
             "Dampens high frequency (100x isn't 100x more important)"],
            ["Double Normalization", "0.5 + 0.5 * f/max_f",
             "Scales TF to [0.5, 1.0] range"],
            ["Smoothed IDF", "log((N+1)/(df+1)) + 1",
             "Prevents negatives, handles edge cases"],
            ["BM25", "Probabilistic ranking",
             "Term saturation; used by Elasticsearch"],
        ], ACCENT_RED)

    add_table_slide(prs, "TF-IDF vs. Other Methods",
        ["Method", "Description", "When to Use"],
        [
            ["TF-IDF", "Statistical word importance",
             "Keyword extraction, simple search"],
            ["BM25", "Probabilistic TF-IDF variant",
             "Production search engines"],
            ["Word2Vec", "Neural word embeddings",
             "Semantic similarity"],
            ["BERT", "Contextual embeddings",
             "State-of-the-art NLP tasks"],
        ], ACCENT_RED)

    # ── References ──
    add_section_slide(prs, "6. References", ACCENT_RED)
    add_content_slide(prs, "Key References", [
        "[1] Sparck Jones (1972) - 'A statistical interpretation of term specificity' "
        "-- Foundation paper introducing IDF",
        "",
        "[2] Salton & Buckley (1988) - 'Term-weighting approaches in automatic "
        "text retrieval' -- Established TF-IDF best practices",
        "",
        "[3] Robertson (2004) - 'Understanding inverse document frequency' "
        "-- Probabilistic justifications for why IDF works",
        "",
        "[4] Manning, Raghavan & Schutze (2008) - 'Introduction to Information "
        "Retrieval' -- Definitive textbook (freely available online)",
    ], ACCENT_RED)


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════

def main() -> None:
    """Generate 6 PPTX files, one per topic."""
    output_dir = "../resources"

    topics = [
        ("llm_prompt_engineering", build_llm_prompt_engineering),
        ("methods_comparison", build_methods_comparison),
        ("neural_networks", build_neural_networks),
        ("ngram", build_ngram),
        ("pos_tagging", build_pos_tagging),
        ("tfidf", build_tfidf),
    ]

    for name, builder in topics:
        prs = _new_prs()
        builder(prs)
        path = f"{output_dir}/{name}_presentation.pptx"
        prs.save(path)
        print(f"Saved: {path}  ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
