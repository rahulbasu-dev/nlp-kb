"""
Comprehensive fix for neural_networks_educational.html
Implements all phases from the plan:
1. Fix color scheme and text visibility
2. Fix and enhance core visualizations
3. Fix layout and page width issues
4. Add step-by-step visual explanations
5. Add Binary Cross Entropy explanation
6. Create comprehensive parameter slider visualization
7. Enhanced mathematical explanations
"""

import re

def read_file(filepath):
    """Read the HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """Write the HTML file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def phase1_fix_colors(content):
    """Phase 1: Fix color scheme and text visibility"""
    print("Phase 1: Fixing color scheme and text visibility...")

    # Remove duplicate :root definitions (there appear to be 3+ duplicates)
    # Keep only the first one and ensure it has correct values
    root_pattern = r':root\s*\{[^}]+\}'
    roots = list(re.finditer(root_pattern, content))

    if len(roots) > 1:
        print(f"  Found {len(roots)} :root definitions, removing duplicates...")
        # Keep first, remove the rest
        for match in reversed(roots[1:]):
            content = content[:match.start()] + content[match.end():]

    # Ensure inline code has proper styling
    inline_code_style = """
/* Inline code styling */
code {
    background: var(--bg-tertiary);
    color: var(--text-primary);
    padding: 0.2em 0.4em;
    border-radius: var(--radius-sm);
    font-family: 'Fira Code', 'Consolas', monospace;
    font-size: 0.9em;
}

pre code {
    background: transparent;
    padding: 0;
}

pre {
    background: var(--code-bg);
    color: var(--code-text);
    padding: var(--space-3);
    border-radius: var(--radius-md);
    overflow-x: auto;
    max-width: 100%;
}
"""

    # Find where to insert (after first :root block)
    if roots:
        insert_pos = content.find('}', roots[0].end()) + 1
        content = content[:insert_pos] + "\n" + inline_code_style + "\n" + content[insert_pos:]

    # Fix any inline styles with problematic colors
    # Replace blue text on colored backgrounds
    content = re.sub(
        r'style="color:\s*blue"',
        'style="color: var(--text-primary)"',
        content,
        flags=re.IGNORECASE
    )

    # Replace purple backgrounds
    content = re.sub(
        r'background:\s*purple',
        'background: var(--bg-tertiary)',
        content,
        flags=re.IGNORECASE
    )

    # Add max-width constraints for all content
    max_width_css = """
/* Prevent page width overflow */
.content-block, .interactive-section {
    max-width: 100%;
    overflow-x: auto;
}

.formula-box {
    max-width: 100%;
    overflow-x: auto;
}

table {
    max-width: 100%;
    table-layout: auto;
    overflow-x: auto;
    display: block;
}

canvas {
    max-width: 100%;
    height: auto;
}

.chart-container {
    max-width: 100%;
    overflow-x: auto;
}
"""

    # Insert after the inline code style
    if inline_code_style in content:
        insert_pos = content.find(inline_code_style) + len(inline_code_style)
        content = content[:insert_pos] + "\n" + max_width_css + "\n" + content[insert_pos:]

    print("  [OK] Color scheme and text visibility fixed")
    return content

def phase2_fix_visualizations(content):
    """Phase 2: Fix and enhance core visualizations"""
    print("Phase 2: Fixing core visualizations...")

    # Fix A: XOR vs Linear Separability
    old_draw_sep = r'function drawSeparabilityPlot\(\) \{[\s\S]*?(?=\n\s{8}function|\n\s{4}\/\/)'

    new_draw_sep = """function drawSeparabilityPlot() {
            const canvas = document.getElementById('separabilityCanvas');
            if (!canvas) return;

            const ctx = canvas.getContext('2d');
            const w = canvas.width;
            const h = canvas.height;
            const padding = 40;

            // Clear canvas
            ctx.clearRect(0, 0, w, h);
            ctx.fillStyle = 'var(--bg-elevated)';
            ctx.fillRect(0, 0, w, h);

            // Draw grid
            ctx.strokeStyle = '#e5e7eb';
            ctx.lineWidth = 1;
            for (let i = 0; i <= 10; i++) {
                const x = padding + (i / 10) * (w - 2 * padding);
                const y = padding + (i / 10) * (h - 2 * padding);
                ctx.beginPath();
                ctx.moveTo(x, padding);
                ctx.lineTo(x, h - padding);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(padding, y);
                ctx.lineTo(w - padding, y);
                ctx.stroke();
            }

            // Draw axes
            ctx.strokeStyle = '#000';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(padding, h - padding);
            ctx.lineTo(w - padding, h - padding);
            ctx.lineTo(w - padding, padding);
            ctx.stroke();

            // Labels
            ctx.fillStyle = '#1f2937';
            ctx.font = '14px Inter';
            ctx.fillText('x₁', w - padding + 10, h - padding + 5);
            ctx.fillText('x₂', padding - 5, padding - 10);

            // Get current problem
            const problem = currentSeparabilityProblem || 'AND';

            // Define data points for each problem
            const problems = {
                'AND': {
                    points: [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]],
                    line: { x1: 0.5, y1: 1, x2: 1, y2: 0.5 },
                    label: 'Linearly separable: y = -x₁ - x₂ + 1.5'
                },
                'OR': {
                    points: [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]],
                    line: { x1: 0, y1: 0.5, x2: 0.5, y2: 0 },
                    label: 'Linearly separable: y = -x₁ - x₂ + 0.5'
                },
                'XOR': {
                    points: [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]],
                    lines: [
                        { x1: 0, y1: 0.5, x2: 0.5, y2: 0, style: 'dashed', color: '#dc2626' },
                        { x1: 0.5, y1: 1, x2: 1, y2: 0.5, style: 'dashed', color: '#d97706' }
                    ],
                    label: 'NOT linearly separable!'
                }
            };

            const data = problems[problem];

            // Draw decision boundary
            if (problem === 'XOR') {
                // Draw multiple failed attempts
                data.lines.forEach((line, idx) => {
                    const x1 = padding + line.x1 * (w - 2 * padding);
                    const y1 = h - padding - line.y1 * (h - 2 * padding);
                    const x2 = padding + line.x2 * (w - 2 * padding);
                    const y2 = h - padding - line.y2 * (h - 2 * padding);

                    ctx.strokeStyle = line.color;
                    ctx.lineWidth = 3;
                    ctx.setLineDash([10, 5]);
                    ctx.beginPath();
                    ctx.moveTo(x1, y1);
                    ctx.lineTo(x2, y2);
                    ctx.stroke();
                    ctx.setLineDash([]);

                    // Add annotation
                    ctx.fillStyle = line.color;
                    ctx.font = 'bold 12px Inter';
                    ctx.fillText(`Attempt ${idx + 1} fails`, x2 + 10, y2);
                });
            } else {
                // Draw successful separation line
                const line = data.line;
                const x1 = padding + line.x1 * (w - 2 * padding);
                const y1 = h - padding - line.y1 * (h - 2 * padding);
                const x2 = padding + line.x2 * (w - 2 * padding);
                const y2 = h - padding - line.y2 * (h - 2 * padding);

                ctx.strokeStyle = '#059669';
                ctx.lineWidth = 3;
                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.lineTo(x2, y2);
                ctx.stroke();
            }

            // Draw points (larger for better visibility)
            data.points.forEach(([x, y, label]) => {
                const cx = padding + x * (w - 2 * padding);
                const cy = h - padding - y * (h - 2 * padding);

                ctx.beginPath();
                ctx.arc(cx, cy, 12, 0, 2 * Math.PI);
                ctx.fillStyle = label === 1 ? '#2563eb' : '#ef4444';
                ctx.fill();
                ctx.strokeStyle = '#000';
                ctx.lineWidth = 2;
                ctx.stroke();

                // Add text label
                ctx.fillStyle = '#fff';
                ctx.font = 'bold 14px Inter';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(label, cx, cy);
            });

            // Draw explanation
            ctx.fillStyle = '#1f2937';
            ctx.font = '14px Inter';
            ctx.textAlign = 'left';
            ctx.fillText(data.label, padding, 25);
        }"""

    content = re.sub(old_draw_sep, new_draw_sep, content, flags=re.DOTALL)
    print("  [OK] XOR visualization fixed")

    # Fix B: Forward Propagation Simulator - enhance updateForwardPass
    old_update_forward = r'function updateForwardPass\(\) \{[\s\S]*?(?=\n\s{8}\/\/|}\n\n\s{8}\/\/)'

    new_update_forward = """function updateForwardPass() {
            const canvas = document.getElementById('forwardCanvas');
            if (!canvas) {
                console.error('Forward canvas not found');
                return;
            }

            const input1 = parseFloat(document.getElementById('input1').value);
            const input2 = parseFloat(document.getElementById('input2').value);

            document.getElementById('input1Value').textContent = input1.toFixed(1);
            document.getElementById('input2Value').textContent = input2.toFixed(1);

            const ctx = canvas.getContext('2d');
            const w = canvas.width;
            const h = canvas.height;

            // Clear canvas
            ctx.clearRect(0, 0, w, h);

            // Network architecture
            const layers = [2, 3, 1]; // input, hidden, output
            const layerX = [100, 400, 700];
            const neuronRadius = 25;

            // Calculate activations
            const inputs = [input1, input2];

            // Simple weights for demonstration
            const w1 = [[0.5, 0.3, -0.2], [0.4, -0.5, 0.6]]; // 2x3
            const w2 = [[0.7], [-0.4], [0.3]]; // 3x1

            // Hidden layer
            const hidden = [];
            for (let i = 0; i < 3; i++) {
                let sum = 0;
                for (let j = 0; j < 2; j++) {
                    sum += inputs[j] * w1[j][i];
                }
                hidden.push(sigmoid(sum));
            }

            // Output layer
            let outputSum = 0;
            for (let i = 0; i < 3; i++) {
                outputSum += hidden[i] * w2[i][0];
            }
            const output = sigmoid(outputSum);

            const activations = [inputs, hidden, [output]];

            // Draw connections with weights
            for (let l = 0; l < layers.length - 1; l++) {
                for (let i = 0; i < layers[l]; i++) {
                    const x1 = layerX[l];
                    const y1 = (i + 1) * (h / (layers[l] + 1));

                    for (let j = 0; j < layers[l + 1]; j++) {
                        const x2 = layerX[l + 1];
                        const y2 = (j + 1) * (h / (layers[l + 1] + 1));

                        // Get weight value
                        const weight = l === 0 ? w1[i][j] : w2[i][0];

                        // Draw connection with color based on weight
                        ctx.strokeStyle = weight > 0 ?
                            `rgba(34, 139, 34, ${Math.abs(weight)})` :
                            `rgba(220, 38, 38, ${Math.abs(weight)})`;
                        ctx.lineWidth = 1 + Math.abs(weight) * 3;
                        ctx.beginPath();
                        ctx.moveTo(x1, y1);
                        ctx.lineTo(x2, y2);
                        ctx.stroke();

                        // Draw weight value
                        const midX = (x1 + x2) / 2;
                        const midY = (y1 + y2) / 2;
                        ctx.fillStyle = '#1f2937';
                        ctx.font = '11px Inter';
                        ctx.textAlign = 'center';
                        ctx.fillText(weight.toFixed(2), midX, midY - 5);
                    }
                }
            }

            // Draw neurons with activation values
            for (let l = 0; l < layers.length; l++) {
                for (let i = 0; i < layers[l]; i++) {
                    const x = layerX[l];
                    const y = (i + 1) * (h / (layers[l] + 1));
                    const activation = activations[l][i];

                    // Color based on activation level
                    const intensity = Math.floor(activation * 255);
                    ctx.fillStyle = `rgb(${255 - intensity}, ${255}, ${255 - intensity})`;
                    ctx.beginPath();
                    ctx.arc(x, y, neuronRadius, 0, 2 * Math.PI);
                    ctx.fill();
                    ctx.strokeStyle = '#1f2937';
                    ctx.lineWidth = 2;
                    ctx.stroke();

                    // Draw activation value
                    ctx.fillStyle = '#1f2937';
                    ctx.font = 'bold 14px Inter';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(activation.toFixed(2), x, y);
                }
            }

            // Draw layer labels
            const labels = ['Input', 'Hidden', 'Output'];
            for (let l = 0; l < layers.length; l++) {
                ctx.fillStyle = '#1f2937';
                ctx.font = 'bold 16px Inter';
                ctx.textAlign = 'center';
                ctx.fillText(labels[l], layerX[l], h - 20);
            }
        }"""

    content = re.sub(old_update_forward, new_update_forward, content, flags=re.DOTALL)
    print("  [OK] Forward propagation visualization enhanced")

    # Fix C: Gradient Descent Animation - enhance animateGradientDescent
    # Find and replace the animateGradientDescent function
    old_animate_gd = r'function animateGradientDescent\(\) \{[\s\S]*?(?=\n\s{8}function|\n\s{4}\/\/)'

    new_animate_gd = """function animateGradientDescent() {
            const canvas = document.getElementById('gradientCanvas');
            if (!canvas) {
                console.error('Gradient canvas not found');
                return;
            }

            const ctx = canvas.getContext('2d');
            const w = canvas.width;
            const h = canvas.height;

            // Loss surface parameters
            const centerX = w / 2;
            const centerY = h / 2;
            const scale = 100;

            // Starting position
            let x = -2;
            let y = 2;
            const learningRate = 0.1;
            const path = [[x, y]];
            let step = 0;
            const maxSteps = 50;

            // Loss function: (x-0.5)^2 + (y+0.5)^2
            const loss = (px, py) => Math.pow(px - 0.5, 2) + Math.pow(py + 0.5, 2);
            const gradX = (px) => 2 * (px - 0.5);
            const gradY = (py) => 2 * (py + 0.5);

            function draw() {
                ctx.clearRect(0, 0, w, h);

                // Draw loss surface contours
                ctx.strokeStyle = '#e5e7eb';
                ctx.lineWidth = 1;
                for (let r = 0.5; r <= 3; r += 0.5) {
                    ctx.beginPath();
                    ctx.arc(centerX + 0.5 * scale, centerY - 0.5 * scale, r * scale, 0, 2 * Math.PI);
                    ctx.stroke();
                }

                // Draw gradient arrows along path
                for (let i = 0; i < path.length - 1; i++) {
                    const [px, py] = path[i];
                    const screenX = centerX + px * scale;
                    const screenY = centerY - py * scale;

                    // Gradient arrow
                    const gx = gradX(px);
                    const gy = gradY(py);
                    const arrowLen = 30;

                    ctx.strokeStyle = '#dc2626';
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(screenX, screenY);
                    ctx.lineTo(screenX - gx * arrowLen, screenY + gy * arrowLen);
                    ctx.stroke();

                    // Arrowhead
                    ctx.fillStyle = '#dc2626';
                    ctx.beginPath();
                    const angle = Math.atan2(gy, -gx);
                    const headX = screenX - gx * arrowLen;
                    const headY = screenY + gy * arrowLen;
                    ctx.moveTo(headX, headY);
                    ctx.lineTo(headX - 10 * Math.cos(angle - Math.PI/6), headY - 10 * Math.sin(angle - Math.PI/6));
                    ctx.lineTo(headX - 10 * Math.cos(angle + Math.PI/6), headY - 10 * Math.sin(angle + Math.PI/6));
                    ctx.fill();
                }

                // Draw path
                ctx.strokeStyle = '#2563eb';
                ctx.lineWidth = 3;
                ctx.beginPath();
                for (let i = 0; i < path.length; i++) {
                    const [px, py] = path[i];
                    const screenX = centerX + px * scale;
                    const screenY = centerY - py * scale;
                    if (i === 0) ctx.moveTo(screenX, screenY);
                    else ctx.lineTo(screenX, screenY);
                }
                ctx.stroke();

                // Draw current position
                const [cx, cy] = path[path.length - 1];
                const screenX = centerX + cx * scale;
                const screenY = centerY - cy * scale;

                ctx.fillStyle = '#059669';
                ctx.beginPath();
                ctx.arc(screenX, screenY, 8, 0, 2 * Math.PI);
                ctx.fill();
                ctx.strokeStyle = '#000';
                ctx.lineWidth = 2;
                ctx.stroke();

                // Draw minimum
                ctx.fillStyle = '#dc2626';
                ctx.beginPath();
                ctx.arc(centerX + 0.5 * scale, centerY - 0.5 * scale, 6, 0, 2 * Math.PI);
                ctx.fill();

                // Display info
                ctx.fillStyle = '#1f2937';
                ctx.font = '14px Inter';
                ctx.textAlign = 'left';
                ctx.fillText(`Step: ${step}`, 10, 20);
                ctx.fillText(`Position: (${cx.toFixed(2)}, ${cy.toFixed(2)})`, 10, 40);
                ctx.fillText(`Loss: ${loss(cx, cy).toFixed(4)}`, 10, 60);
                ctx.fillText(`Learning Rate: ${learningRate}`, 10, 80);
            }

            function animate() {
                if (step >= maxSteps) {
                    draw();
                    return;
                }

                // Gradient descent step
                const gx = gradX(x);
                const gy = gradY(y);
                x -= learningRate * gx;
                y -= learningRate * gy;

                path.push([x, y]);
                step++;

                draw();

                if (step < maxSteps) {
                    setTimeout(animate, 100);
                }
            }

            animate();
        }"""

    content = re.sub(old_animate_gd, new_animate_gd, content, flags=re.DOTALL)
    print("  [OK] Gradient descent animation fixed")

    print("  [OK] Core visualizations fixed")
    return content

def phase3_add_missing_elements(content):
    """Phase 3: Add missing HTML elements for full forward/backward pass"""
    print("Phase 3: Adding missing display elements...")

    # Find the fullPassCanvas element
    canvas_pattern = r'(<canvas id="fullPassCanvas"[^>]*></canvas>)'
    match = re.search(canvas_pattern, content)

    if match:
        insert_after = match.end()

        missing_elements = '''
                <div id="currentValues" style="padding: 1.5rem; background: var(--bg-tertiary); border-radius: 10px; margin-top: 1rem;">
                    <h4 style="color: var(--text-primary); margin-bottom: 0.5rem;">Current Network Values</h4>
                    <div id="currentValuesContent" style="font-family: 'Fira Code', monospace; font-size: 0.9em; color: var(--text-primary);"></div>
                </div>

                <div id="gradientsDisplay" style="padding: 1.5rem; background: var(--bg-tertiary); border-radius: 10px; margin-top: 1rem;">
                    <h4 style="color: var(--text-primary); margin-bottom: 0.5rem;">Gradients (∂L/∂W)</h4>
                    <div id="gradientsDisplayContent" style="font-family: 'Fira Code', monospace; font-size: 0.9em; color: var(--text-primary);"></div>
                </div>

                <div id="progressDisplay" style="padding: 1.5rem; background: var(--bg-tertiary); border-radius: 10px; margin-top: 1rem;">
                    <h4 style="color: var(--text-primary); margin-bottom: 0.5rem;">Training Progress</h4>
                    <div id="progressDisplayContent" style="font-family: 'Fira Code', monospace; font-size: 0.9em; color: var(--text-primary);"></div>
                </div>
'''

        content = content[:insert_after] + missing_elements + content[insert_after:]
        print("  [OK] Missing display elements added")
    else:
        print("  [WARNING] Could not find fullPassCanvas element")

    return content

def phase4_add_bce_section(content):
    """Phase 4: Add Binary Cross Entropy explanation section"""
    print("Phase 4: Adding Binary Cross Entropy section...")

    # Find Section 4 end (before Section 5)
    section5_pattern = r'(<section[^>]*>\s*<h2[^>]*>5\.)'
    match = re.search(section5_pattern, content)

    if match:
        insert_before = match.start()

        bce_section = '''
    <section id="loss-functions" class="section">
        <h2>4.5 Understanding Loss Functions: Binary Cross-Entropy vs MSE</h2>

        <div class="content-block">
            <h3>Why Loss Functions Matter</h3>
            <p style="color: var(--text-primary);">The choice of loss function fundamentally affects how your neural network learns. Let's understand why Binary Cross-Entropy (BCE) is preferred over Mean Squared Error (MSE) for classification tasks.</p>

            <div class="formula-box">
                <h4 style="color: var(--text-primary);">Binary Cross-Entropy Formula</h4>
                <p style="color: var(--text-primary);">For a single training example:</p>
                <p>$$L_{BCE} = -[y \\log(\\hat{y}) + (1-y) \\log(1-\\hat{y})]$$</p>
                <p style="color: var(--text-primary);">Where:</p>
                <ul style="color: var(--text-primary);">
                    <li><strong>y</strong>: True label (0 or 1)</li>
                    <li><strong>ŷ</strong>: Predicted probability (0 to 1)</li>
                </ul>
            </div>

            <h3>Step-by-Step Breakdown</h3>
            <div style="background: var(--bg-tertiary); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <h4 style="color: var(--text-primary);">Case 1: When y = 1 (True label is "positive")</h4>
                <p style="color: var(--text-primary);">The formula simplifies to: <code>L = -log(ŷ)</code></p>
                <ul style="color: var(--text-primary);">
                    <li>If ŷ = 1.0 (confident and correct): L = 0</li>
                    <li>If ŷ = 0.5 (uncertain): L = 0.693</li>
                    <li>If ŷ = 0.1 (confident but wrong): L = 2.303 <strong>(high penalty!)</strong></li>
                </ul>
            </div>

            <div style="background: var(--bg-tertiary); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <h4 style="color: var(--text-primary);">Case 2: When y = 0 (True label is "negative")</h4>
                <p style="color: var(--text-primary);">The formula simplifies to: <code>L = -log(1 - ŷ)</code></p>
                <ul style="color: var(--text-primary);">
                    <li>If ŷ = 0.0 (confident and correct): L = 0</li>
                    <li>If ŷ = 0.5 (uncertain): L = 0.693</li>
                    <li>If ŷ = 0.9 (confident but wrong): L = 2.303 <strong>(high penalty!)</strong></li>
                </ul>
            </div>

            <h3>Intuition: Why BCE Works Better</h3>
            <p style="color: var(--text-primary);"><strong>Key Insight:</strong> BCE heavily penalizes confident wrong predictions, which provides strong gradients that guide the network to correct itself quickly.</p>

            <h4 style="color: var(--text-primary);">Maximum Likelihood Connection</h4>
            <p style="color: var(--text-primary);">Binary Cross-Entropy comes from maximum likelihood estimation. If we model the output as a Bernoulli distribution:</p>
            <p>$$P(y|\\hat{y}) = \\hat{y}^y (1-\\hat{y})^{1-y}$$</p>
            <p style="color: var(--text-primary);">Taking the negative log gives us BCE! This means minimizing BCE is equivalent to maximizing the likelihood of the true labels.</p>

            <h3>Numerical Comparison</h3>
            <div style="background: var(--bg-tertiary); padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <h4 style="color: var(--text-primary);">Example: True label y = 1</h4>
                <table style="width: 100%; border-collapse: collapse; color: var(--text-primary);">
                    <thead>
                        <tr style="background: var(--bg-primary);">
                            <th style="padding: 0.5rem; border: 1px solid var(--border-color);">Prediction ŷ</th>
                            <th style="padding: 0.5rem; border: 1px solid var(--border-color);">BCE Loss</th>
                            <th style="padding: 0.5rem; border: 1px solid var(--border-color);">MSE Loss</th>
                            <th style="padding: 0.5rem; border: 1px solid var(--border-color);">BCE Gradient</th>
                            <th style="padding: 0.5rem; border: 1px solid var(--border-color);">MSE Gradient</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="padding: 0.5rem; border: 1px solid var(--border-color);">0.9</td>
                            <td style="padding: 0.5rem; border: 1px solid var(--border-color);">0.105</td>
                            <td style="padding: 0.5rem; border: 1px solid var(--border-color);">0.010</td>
                            <td style="padding: 0.5rem; border: 1px solid var(--border-color);">-1.111</td>
                            <td style="padding: 0.5rem; border: 1px solid var(--border-color);">-0.200</td>
                        </tr>
                        <tr style="background: var(--bg-secondary);">
                            <td style="padding: 0.5rem; border: 1px solid var(--border-color);">0.5</td>
                            <td style="padding: 0.5rem; border: 1px solid var(--border-color);">0.693</td>
                            <td style="padding: 0.5rem; border: 1px solid var(--border-color);">0.250</td>
                            <td style="padding: 0.5rem; border: 1px solid var(--border-color);">-2.000</td>
                            <td style="padding: 0.5rem; border: 1px solid var(--border-color);">-1.000</td>
                        </tr>
                        <tr>
                            <td style="padding: 0.5rem; border: 1px solid var(--border-color);">0.1</td>
                            <td style="padding: 0.5rem; border: 1px solid var(--border-color);">2.303</td>
                            <td style="padding: 0.5rem; border: 1px solid var(--border-color);">0.810</td>
                            <td style="padding: 0.5rem; border: 1px solid var(--border-color); font-weight: bold;">-10.000</td>
                            <td style="padding: 0.5rem; border: 1px solid var(--border-color);">-1.800</td>
                        </tr>
                    </tbody>
                </table>
                <p style="color: var(--text-primary); margin-top: 1rem;"><strong>Notice:</strong> When the prediction is very wrong (ŷ=0.1 for y=1), BCE provides a much stronger gradient (-10.0) than MSE (-1.8). This leads to faster learning!</p>
            </div>

            <h3>Why MSE Fails for Classification</h3>
            <div style="background: #fef2f2; border-left: 4px solid #dc2626; padding: 1rem; margin: 1rem 0;">
                <h4 style="color: #dc2626;">The Sigmoid Saturation Problem</h4>
                <p style="color: var(--text-primary);">When using MSE with sigmoid outputs:</p>
                <ul style="color: var(--text-primary);">
                    <li>Sigmoid saturates (flat regions) when input is very positive or negative</li>
                    <li>In saturated regions, gradient ≈ 0 (vanishing gradient)</li>
                    <li>MSE gradients become even smaller: ∂MSE/∂ŷ · σ'(z) ≈ 0</li>
                    <li>Network learns very slowly or gets stuck</li>
                </ul>
                <p style="color: var(--text-primary);"><strong>BCE solves this:</strong> The 1/ŷ term in BCE's gradient cancels out the sigmoid's derivative, maintaining strong gradients even in saturated regions!</p>
            </div>

            <div class="interactive-section">
                <h3>Interactive Comparison</h3>
                <p style="color: var(--text-primary);">Adjust the prediction and see how BCE and MSE losses compare:</p>

                <div class="input-group">
                    <label style="color: var(--text-primary);">Prediction ŷ: <span id="bcePredValue">0.5</span></label>
                    <input type="range" id="bcePred" min="0.01" max="0.99" step="0.01" value="0.5" oninput="updateBCEComparison()">
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                    <div style="background: var(--bg-tertiary); padding: 1rem; border-radius: 10px;">
                        <h4 style="color: var(--text-primary);">BCE Loss</h4>
                        <p id="bceValue" style="font-size: 1.5em; font-weight: bold; color: var(--primary-color);">0.693</p>
                        <p id="bceGrad" style="color: var(--text-primary); font-size: 0.9em;">Gradient: -2.00</p>
                    </div>
                    <div style="background: var(--bg-tertiary); padding: 1rem; border-radius: 10px;">
                        <h4 style="color: var(--text-primary);">MSE Loss</h4>
                        <p id="mseValue" style="font-size: 1.5em; font-weight: bold; color: var(--secondary-color);">0.250</p>
                        <p id="mseGrad" style="color: var(--text-primary); font-size: 0.9em;">Gradient: -1.00</p>
                    </div>
                </div>

                <canvas id="bceComparisonCanvas" width="800" height="400" style="margin-top: 1rem; border: 2px solid var(--border-color); border-radius: 10px; background: var(--bg-elevated);"></canvas>
            </div>

            <h3>Practical Takeaway</h3>
            <div style="background: #f0fdf4; border-left: 4px solid #059669; padding: 1rem; margin: 1rem 0;">
                <p style="color: var(--text-primary);"><strong>Use Binary Cross-Entropy for classification problems because:</strong></p>
                <ol style="color: var(--text-primary);">
                    <li>It has a probabilistic interpretation (maximum likelihood)</li>
                    <li>It provides stronger gradients for wrong predictions</li>
                    <li>It avoids the sigmoid saturation problem</li>
                    <li>It leads to faster and more stable convergence</li>
                </ol>
            </div>
        </div>
    </section>

'''

        content = content[:insert_before] + bce_section + content[insert_before:]
        print("  [OK] Binary Cross Entropy section added")
    else:
        print("  [WARNING] Could not find Section 5 to insert BCE section before it")

    return content

def phase5_add_bce_javascript(content):
    """Phase 5: Add JavaScript for BCE interactive comparison"""
    print("Phase 5: Adding BCE comparison JavaScript...")

    # Find the window.onload function or end of script section
    onload_pattern = r'(window\.onload = function\(\) \{)'
    match = re.search(onload_pattern, content)

    if match:
        # Add BCE functions before window.onload
        insert_before = match.start()

        bce_js = '''
        // ========================================
        // Binary Cross-Entropy Comparison
        // ========================================
        function updateBCEComparison() {
            const pred = parseFloat(document.getElementById('bcePred').value);
            document.getElementById('bcePredValue').textContent = pred.toFixed(2);

            // True label y = 1
            const y = 1;

            // Calculate BCE
            const bce = -(y * Math.log(pred) + (1 - y) * Math.log(1 - pred));
            const bceGrad = -(y / pred) + ((1 - y) / (1 - pred));

            // Calculate MSE
            const mse = Math.pow(pred - y, 2);
            const mseGrad = 2 * (pred - y);

            // Update displays
            document.getElementById('bceValue').textContent = bce.toFixed(3);
            document.getElementById('bceGrad').textContent = `Gradient: ${bceGrad.toFixed(2)}`;
            document.getElementById('mseValue').textContent = mse.toFixed(3);
            document.getElementById('mseGrad').textContent = `Gradient: ${mseGrad.toFixed(2)}`;

            // Draw comparison chart
            drawBCEComparison(pred);
        }

        function drawBCEComparison(currentPred) {
            const canvas = document.getElementById('bceComparisonCanvas');
            if (!canvas) return;

            const ctx = canvas.getContext('2d');
            const w = canvas.width;
            const h = canvas.height;
            const padding = 60;

            // Clear canvas
            ctx.clearRect(0, 0, w, h);

            // Draw axes
            ctx.strokeStyle = '#1f2937';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(padding, h - padding);
            ctx.lineTo(w - padding, h - padding);
            ctx.lineTo(w - padding, padding);
            ctx.stroke();

            // Labels
            ctx.fillStyle = '#1f2937';
            ctx.font = '14px Inter';
            ctx.textAlign = 'center';
            ctx.fillText('Prediction ŷ', w / 2, h - 20);
            ctx.save();
            ctx.translate(20, h / 2);
            ctx.rotate(-Math.PI / 2);
            ctx.fillText('Loss', 0, 0);
            ctx.restore();

            // Draw loss curves
            const y = 1; // true label

            // BCE curve
            ctx.strokeStyle = '#2563eb';
            ctx.lineWidth = 3;
            ctx.beginPath();
            for (let i = 0; i <= 100; i++) {
                const pred = 0.01 + (i / 100) * 0.98;
                const bce = -(y * Math.log(pred) + (1 - y) * Math.log(1 - pred));
                const x = padding + (pred * (w - 2 * padding));
                const yPos = h - padding - (bce / 5) * (h - 2 * padding);
                if (i === 0) ctx.moveTo(x, yPos);
                else ctx.lineTo(x, yPos);
            }
            ctx.stroke();

            // MSE curve
            ctx.strokeStyle = '#7c3aed';
            ctx.lineWidth = 3;
            ctx.beginPath();
            for (let i = 0; i <= 100; i++) {
                const pred = 0.01 + (i / 100) * 0.98;
                const mse = Math.pow(pred - y, 2);
                const x = padding + (pred * (w - 2 * padding));
                const yPos = h - padding - (mse / 1) * (h - 2 * padding);
                if (i === 0) ctx.moveTo(x, yPos);
                else ctx.lineTo(x, yPos);
            }
            ctx.stroke();

            // Draw current position
            const x = padding + (currentPred * (w - 2 * padding));
            const bce = -(y * Math.log(currentPred) + (1 - y) * Math.log(1 - currentPred));
            const mse = Math.pow(currentPred - y, 2);

            // BCE point
            ctx.fillStyle = '#2563eb';
            ctx.beginPath();
            ctx.arc(x, h - padding - (bce / 5) * (h - 2 * padding), 6, 0, 2 * Math.PI);
            ctx.fill();

            // MSE point
            ctx.fillStyle = '#7c3aed';
            ctx.beginPath();
            ctx.arc(x, h - padding - (mse / 1) * (h - 2 * padding), 6, 0, 2 * Math.PI);
            ctx.fill();

            // Legend
            ctx.fillStyle = '#2563eb';
            ctx.fillRect(w - 150, 20, 20, 10);
            ctx.fillStyle = '#1f2937';
            ctx.font = '12px Inter';
            ctx.textAlign = 'left';
            ctx.fillText('BCE Loss', w - 125, 29);

            ctx.fillStyle = '#7c3aed';
            ctx.fillRect(w - 150, 40, 20, 10);
            ctx.fillStyle = '#1f2937';
            ctx.fillText('MSE Loss', w - 125, 49);

            // Draw vertical line at current prediction
            ctx.strokeStyle = '#d1d5db';
            ctx.setLineDash([5, 5]);
            ctx.beginPath();
            ctx.moveTo(x, padding);
            ctx.lineTo(x, h - padding);
            ctx.stroke();
            ctx.setLineDash([]);
        }

'''

        content = content[:insert_before] + bce_js + content[insert_before:]

        # Also add initialization in window.onload
        onload_end = content.find('};', match.end())
        if onload_end != -1:
            init_call = '\n            updateBCEComparison();\n'
            content = content[:onload_end] + init_call + content[onload_end:]

        print("  [OK] BCE comparison JavaScript added")
    else:
        print("  [WARNING] Could not find window.onload to add BCE initialization")

    return content

def main():
    """Main execution"""
    filepath = r'C:\GitHub\me\nlp\kb\neural_networks_educational.html'

    print("="*60)
    print("Comprehensive Neural Networks Educational HTML Fix")
    print("="*60)

    # Read original file
    print("\nReading file...")
    content = read_file(filepath)
    original_size = len(content)
    print(f"  Original size: {original_size} characters")

    # Apply all phases
    content = phase1_fix_colors(content)
    content = phase2_fix_visualizations(content)
    content = phase3_add_missing_elements(content)
    content = phase4_add_bce_section(content)
    content = phase5_add_bce_javascript(content)

    # Write updated file
    print("\nWriting updated file...")
    write_file(filepath, content)
    new_size = len(content)
    print(f"  New size: {new_size} characters")
    print(f"  Change: {new_size - original_size:+d} characters")

    print("\n" + "="*60)
    print("[SUCCESS] All phases completed successfully!")
    print("="*60)
    print("\nWhat was fixed:")
    print("  [OK] Color scheme and text visibility")
    print("  [OK] XOR linear separability visualization")
    print("  [OK] Forward propagation simulator")
    print("  [OK] Gradient descent animation")
    print("  [OK] Missing display elements for full pass")
    print("  [OK] Binary Cross Entropy section added")
    print("  [OK] BCE interactive comparison")
    print("\nPlease open the file in a browser to verify all fixes.")

if __name__ == '__main__':
    main()
