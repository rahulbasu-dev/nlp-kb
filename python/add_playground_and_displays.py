"""
Add missing display elements and create the comprehensive Neural Network Playground
"""

import re

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def add_display_elements(content):
    """Add missing display elements after fullNetworkCanvas"""
    print("Adding missing display elements...")

    # Find the fullNetworkCanvas
    canvas_pattern = r'(<canvas id="fullNetworkCanvas"[^>]*></canvas>)'
    match = re.search(canvas_pattern, content)

    if match:
        # Find the closing </div> after the canvas
        insert_pos = content.find('</div>', match.end())

        if insert_pos != -1:
            display_elements = '''

                <div id="currentValues" style="padding: 1.5rem; background: var(--bg-tertiary); border-radius: 10px; margin-top: 1.5rem;">
                    <h4 style="color: var(--text-primary); margin-bottom: 1rem; font-size: 1.1rem;">📊 Current Network Values</h4>
                    <div id="currentValuesContent" style="font-family: 'Fira Code', monospace; font-size: 0.9em; color: var(--text-primary); line-height: 1.8;"></div>
                </div>

                <div id="gradientsDisplay" style="padding: 1.5rem; background: var(--bg-tertiary); border-radius: 10px; margin-top: 1.5rem;">
                    <h4 style="color: var(--text-primary); margin-bottom: 1rem; font-size: 1.1rem;">📉 Gradients (∂L/∂W)</h4>
                    <div id="gradientsDisplayContent" style="font-family: 'Fira Code', monospace; font-size: 0.9em; color: var(--text-primary); line-height: 1.8;"></div>
                </div>

                <div id="progressDisplay" style="padding: 1.5rem; background: var(--bg-tertiary); border-radius: 10px; margin-top: 1.5rem;">
                    <h4 style="color: var(--text-primary); margin-bottom: 1rem; font-size: 1.1rem;">📈 Training Progress</h4>
                    <div id="progressDisplayContent" style="font-family: 'Fira Code', monospace; font-size: 0.9em; color: var(--text-primary); line-height: 1.8;"></div>
                </div>
'''

            content = content[:insert_pos] + display_elements + content[insert_pos:]
            print("  [OK] Display elements added")
        else:
            print("  [WARNING] Could not find insertion point")
    else:
        print("  [WARNING] Could not find fullNetworkCanvas")

    return content

def add_neural_playground(content):
    """Add comprehensive Neural Network Playground section"""
    print("Adding Neural Network Playground section...")

    # Find where to insert (after section G, before next section)
    # Look for the closing </div> of section G
    pattern = r'(<div id="progressDisplay"[^>]*>[\s\S]*?</div>\s*</div>\s*</div>)'
    match = re.search(pattern, content)

    if not match:
        # Alternative: find after the fullNetworkCanvas section
        pattern = r'(</div>\s*</section>)(?=\s*<section)'
        matches = list(re.finditer(pattern, content))
        if len(matches) >= 3:  # Find 3rd section closing (should be section 2)
            match = matches[2]

    if match:
        insert_pos = match.end()

        playground_html = '''

    <section id="neural-playground" class="section">
        <h2>3. Complete Neural Network Playground 🎮</h2>

        <div class="content-block">
            <p style="color: var(--text-primary);">Explore how every parameter affects network behavior in real-time. Adjust architecture, activation functions, learning rate, and watch the network learn!</p>
        </div>

        <div class="interactive-section">
            <h3>H. Interactive Neural Network Sandbox</h3>

            <canvas id="playgroundCanvas" width="1400" height="800" style="border: 2px solid var(--border-color); border-radius: 10px; background: var(--bg-elevated); display: block; margin: 0 auto; max-width: 100%;"></canvas>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 2rem;">

                <!-- Architecture Controls -->
                <div style="background: var(--bg-tertiary); padding: 1.5rem; border-radius: 10px;">
                    <h4 style="color: var(--text-primary); margin-bottom: 1rem;">🏗️ Architecture</h4>

                    <div style="margin-bottom: 1rem;">
                        <label style="color: var(--text-primary); display: block; margin-bottom: 0.5rem;">
                            Input Neurons: <span id="pgInputSize">2</span>
                        </label>
                        <input type="range" id="pgInputSlider" min="1" max="4" value="2" step="1"
                               oninput="updatePlaygroundArchitecture()" style="width: 100%;">
                    </div>

                    <div style="margin-bottom: 1rem;">
                        <label style="color: var(--text-primary); display: block; margin-bottom: 0.5rem;">
                            Hidden Layers: <span id="pgHiddenLayers">1</span>
                        </label>
                        <input type="range" id="pgHiddenLayersSlider" min="1" max="3" value="1" step="1"
                               oninput="updatePlaygroundArchitecture()" style="width: 100%;">
                    </div>

                    <div style="margin-bottom: 1rem;">
                        <label style="color: var(--text-primary); display: block; margin-bottom: 0.5rem;">
                            Neurons per Hidden: <span id="pgHiddenSize">3</span>
                        </label>
                        <input type="range" id="pgHiddenSizeSlider" min="1" max="8" value="3" step="1"
                               oninput="updatePlaygroundArchitecture()" style="width: 100%;">
                    </div>

                    <div style="margin-bottom: 1rem;">
                        <label style="color: var(--text-primary); display: block; margin-bottom: 0.5rem;">
                            Output Neurons: <span id="pgOutputSize">1</span>
                        </label>
                        <input type="range" id="pgOutputSlider" min="1" max="4" value="1" step="1"
                               oninput="updatePlaygroundArchitecture()" style="width: 100%;">
                    </div>
                </div>

                <!-- Activation Function -->
                <div style="background: var(--bg-tertiary); padding: 1.5rem; border-radius: 10px;">
                    <h4 style="color: var(--text-primary); margin-bottom: 1rem;">⚡ Activation Function</h4>

                    <select id="pgActivation" onchange="updatePlaygroundActivation()"
                            style="width: 100%; padding: 0.5rem; border-radius: 5px; margin-bottom: 1rem;">
                        <option value="sigmoid">Sigmoid: σ(x) = 1/(1+e^-x)</option>
                        <option value="relu">ReLU: max(0, x)</option>
                        <option value="tanh">Tanh: tanh(x)</option>
                        <option value="leaky_relu">Leaky ReLU: max(0.01x, x)</option>
                    </select>

                    <div id="pgActivationFormula" style="background: var(--bg-primary); padding: 1rem; border-radius: 5px; font-size: 0.9em;">
                        <p style="color: var(--text-primary); margin: 0;"><strong>Formula:</strong></p>
                        <p id="pgActivationFormulaText" style="color: var(--text-secondary); margin: 0.5rem 0 0 0;">σ(x) = 1 / (1 + e^(-x))</p>
                    </div>
                </div>

                <!-- Input Values -->
                <div style="background: var(--bg-tertiary); padding: 1.5rem; border-radius: 10px;">
                    <h4 style="color: var(--text-primary); margin-bottom: 1rem;">🎯 Input Values</h4>

                    <div id="pgInputControls"></div>

                    <button onclick="randomizePlaygroundInputs()"
                            style="width: 100%; margin-top: 1rem; padding: 0.75rem; background: var(--primary-color); color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: 600;">
                        🎲 Randomize Inputs
                    </button>
                </div>

                <!-- Training Controls -->
                <div style="background: var(--bg-tertiary); padding: 1.5rem; border-radius: 10px;">
                    <h4 style="color: var(--text-primary); margin-bottom: 1rem;">🎓 Training</h4>

                    <div style="margin-bottom: 1rem;">
                        <label style="color: var(--text-primary); display: block; margin-bottom: 0.5rem;">
                            Learning Rate: <span id="pgLearningRate">0.1</span>
                        </label>
                        <input type="range" id="pgLearningRateSlider" min="0.001" max="1" value="0.1" step="0.001"
                               oninput="updatePlaygroundLearningRate()" style="width: 100%;">
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
                        <button onclick="playgroundStepForward()"
                                style="padding: 0.75rem; background: #10b981; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: 600;">
                            ▶️ Forward
                        </button>
                        <button onclick="playgroundStepBackward()"
                                style="padding: 0.75rem; background: #f59e0b; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: 600;">
                            ◀️ Backward
                        </button>
                    </div>

                    <button onclick="playgroundTrainStep()"
                            style="width: 100%; margin-top: 0.5rem; padding: 0.75rem; background: #8b5cf6; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: 600;">
                        🔄 Full Training Step
                    </button>

                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem; margin-top: 0.5rem;">
                        <button onclick="playgroundTrain(1)"
                                style="padding: 0.5rem; background: var(--primary-color); color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 0.85em; font-weight: 600;">
                            +1
                        </button>
                        <button onclick="playgroundTrain(10)"
                                style="padding: 0.5rem; background: var(--secondary-color); color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 0.85em; font-weight: 600;">
                            +10
                        </button>
                        <button onclick="playgroundTrain(100)"
                                style="padding: 0.5rem; background: var(--accent-color); color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 0.85em; font-weight: 600;">
                            +100
                        </button>
                    </div>
                </div>
            </div>

            <!-- Live Metrics Display -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 2rem; padding: 1.5rem; background: var(--bg-tertiary); border-radius: 10px;">
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.25rem;">Training Steps</div>
                    <div id="pgSteps" style="font-size: 1.8rem; font-weight: bold; color: var(--primary-color);">0</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.25rem;">Current Loss</div>
                    <div id="pgLoss" style="font-size: 1.8rem; font-weight: bold; color: var(--danger-color);">--</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.25rem;">Avg Weight</div>
                    <div id="pgAvgWeight" style="font-size: 1.8rem; font-weight: bold; color: var(--accent-color);">--</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.25rem;">Max Gradient</div>
                    <div id="pgMaxGrad" style="font-size: 1.8rem; font-weight: bold; color: var(--warning-color);">--</div>
                </div>
            </div>

            <!-- Parameter Display Table -->
            <div style="margin-top: 2rem; padding: 1.5rem; background: var(--bg-tertiary); border-radius: 10px;">
                <h4 style="color: var(--text-primary); margin-bottom: 1rem;">📋 Network Parameters</h4>
                <div id="pgParametersTable" style="font-family: 'Fira Code', monospace; font-size: 0.85em; color: var(--text-primary); overflow-x: auto;">
                    <!-- Parameters will be displayed here -->
                </div>
            </div>
        </div>
    </section>

'''

        content = content[:insert_pos] + playground_html + content[insert_pos:]
        print("  [OK] Neural Network Playground section added")
    else:
        print("  [WARNING] Could not find insertion point for playground")

    return content

def add_playground_javascript(content):
    """Add JavaScript for the playground functionality"""
    print("Adding playground JavaScript...")

    # Find window.onload
    onload_pattern = r'(window\.onload = function\(\) \{)'
    match = re.search(onload_pattern, content)

    if match:
        insert_before = match.start()

        playground_js = '''
        // ========================================
        // Neural Network Playground
        // ========================================
        let playgroundState = {
            architecture: { input: 2, hidden: [3], output: 1 },
            activation: 'sigmoid',
            learningRate: 0.1,
            weights: [],
            biases: [],
            inputs: [0.5, 0.5],
            target: [1.0],
            steps: 0,
            currentLoss: 0,
            activations: [],
            gradients: []
        };

        function initializePlaygroundWeights() {
            playgroundState.weights = [];
            playgroundState.biases = [];

            const layers = [
                playgroundState.architecture.input,
                ...playgroundState.architecture.hidden,
                playgroundState.architecture.output
            ];

            for (let i = 0; i < layers.length - 1; i++) {
                const w = [];
                for (let j = 0; j < layers[i]; j++) {
                    const row = [];
                    for (let k = 0; k < layers[i + 1]; k++) {
                        row.push((Math.random() - 0.5) * 2);
                    }
                    w.push(row);
                }
                playgroundState.weights.push(w);

                const b = [];
                for (let j = 0; j < layers[i + 1]; j++) {
                    b.push((Math.random() - 0.5) * 0.2);
                }
                playgroundState.biases.push(b);
            }
        }

        function playgroundActivationFunc(x, func) {
            switch(func) {
                case 'sigmoid': return 1 / (1 + Math.exp(-x));
                case 'relu': return Math.max(0, x);
                case 'tanh': return Math.tanh(x);
                case 'leaky_relu': return x > 0 ? x : 0.01 * x;
                default: return 1 / (1 + Math.exp(-x));
            }
        }

        function playgroundActivationDerivative(x, func) {
            switch(func) {
                case 'sigmoid': {
                    const s = 1 / (1 + Math.exp(-x));
                    return s * (1 - s);
                }
                case 'relu': return x > 0 ? 1 : 0;
                case 'tanh': {
                    const t = Math.tanh(x);
                    return 1 - t * t;
                }
                case 'leaky_relu': return x > 0 ? 1 : 0.01;
                default: {
                    const s = 1 / (1 + Math.exp(-x));
                    return s * (1 - s);
                }
            }
        }

        function updatePlaygroundArchitecture() {
            const inputSize = parseInt(document.getElementById('pgInputSlider').value);
            const hiddenLayers = parseInt(document.getElementById('pgHiddenLayersSlider').value);
            const hiddenSize = parseInt(document.getElementById('pgHiddenSizeSlider').value);
            const outputSize = parseInt(document.getElementById('pgOutputSlider').value);

            document.getElementById('pgInputSize').textContent = inputSize;
            document.getElementById('pgHiddenLayers').textContent = hiddenLayers;
            document.getElementById('pgHiddenSize').textContent = hiddenSize;
            document.getElementById('pgOutputSize').textContent = outputSize;

            playgroundState.architecture = {
                input: inputSize,
                hidden: Array(hiddenLayers).fill(hiddenSize),
                output: outputSize
            };

            // Adjust inputs array
            while (playgroundState.inputs.length < inputSize) {
                playgroundState.inputs.push(0.5);
            }
            playgroundState.inputs = playgroundState.inputs.slice(0, inputSize);

            // Adjust target array
            while (playgroundState.target.length < outputSize) {
                playgroundState.target.push(1.0);
            }
            playgroundState.target = playgroundState.target.slice(0, outputSize);

            initializePlaygroundWeights();
            updatePlaygroundInputControls();
            drawPlayground();
        }

        function updatePlaygroundInputControls() {
            const container = document.getElementById('pgInputControls');
            container.innerHTML = '';

            for (let i = 0; i < playgroundState.inputs.length; i++) {
                const div = document.createElement('div');
                div.style.marginBottom = '0.75rem';
                div.innerHTML = `
                    <label style="color: var(--text-primary); display: block; margin-bottom: 0.25rem; font-size: 0.9em;">
                        Input ${i + 1}: <span id="pgInput${i}Val">${playgroundState.inputs[i].toFixed(2)}</span>
                    </label>
                    <input type="range" id="pgInput${i}" min="-1" max="1" step="0.01" value="${playgroundState.inputs[i]}"
                           oninput="updatePlaygroundInput(${i})" style="width: 100%;">
                `;
                container.appendChild(div);
            }
        }

        function updatePlaygroundInput(index) {
            const value = parseFloat(document.getElementById(`pgInput${index}`).value);
            playgroundState.inputs[index] = value;
            document.getElementById(`pgInput${index}Val`).textContent = value.toFixed(2);
            drawPlayground();
        }

        function randomizePlaygroundInputs() {
            for (let i = 0; i < playgroundState.inputs.length; i++) {
                const value = (Math.random() * 2 - 1);
                playgroundState.inputs[i] = value;
                document.getElementById(`pgInput${i}`).value = value;
                document.getElementById(`pgInput${i}Val`).textContent = value.toFixed(2);
            }
            drawPlayground();
        }

        function updatePlaygroundActivation() {
            playgroundState.activation = document.getElementById('pgActivation').value;

            const formulas = {
                'sigmoid': 'σ(x) = 1 / (1 + e^(-x))',
                'relu': 'ReLU(x) = max(0, x)',
                'tanh': 'tanh(x) = (e^x - e^(-x)) / (e^x + e^(-x))',
                'leaky_relu': 'Leaky ReLU(x) = max(0.01x, x)'
            };

            document.getElementById('pgActivationFormulaText').textContent = formulas[playgroundState.activation];
            drawPlayground();
        }

        function updatePlaygroundLearningRate() {
            const lr = parseFloat(document.getElementById('pgLearningRateSlider').value);
            playgroundState.learningRate = lr;
            document.getElementById('pgLearningRate').textContent = lr.toFixed(3);
        }

        function drawPlayground() {
            const canvas = document.getElementById('playgroundCanvas');
            if (!canvas) return;

            const ctx = canvas.getContext('2d');
            const w = canvas.width;
            const h = canvas.height;

            ctx.clearRect(0, 0, w, h);

            // Calculate layout
            const layers = [
                playgroundState.architecture.input,
                ...playgroundState.architecture.hidden,
                playgroundState.architecture.output
            ];

            const maxNeurons = Math.max(...layers);
            const layerSpacing = Math.min((w - 200) / (layers.length - 1), 300);
            const neuronRadius = Math.min(20, (h - 100) / (maxNeurons * 2.5));

            const layerX = layers.map((_, i) => 100 + i * layerSpacing);

            // Perform forward pass to get activations
            playgroundForwardPass();

            // Draw connections with weights
            for (let l = 0; l < layers.length - 1; l++) {
                for (let i = 0; i < layers[l]; i++) {
                    const y1 = (h / 2) - ((layers[l] - 1) * neuronRadius * 2.5) / 2 + i * neuronRadius * 2.5;

                    for (let j = 0; j < layers[l + 1]; j++) {
                        const y2 = (h / 2) - ((layers[l + 1] - 1) * neuronRadius * 2.5) / 2 + j * neuronRadius * 2.5;

                        const weight = playgroundState.weights[l][i][j];
                        const absWeight = Math.abs(weight);

                        ctx.strokeStyle = weight > 0 ?
                            `rgba(34, 139, 34, ${Math.min(absWeight, 1)})` :
                            `rgba(220, 38, 38, ${Math.min(absWeight, 1)})`;
                        ctx.lineWidth = 1 + absWeight * 2;
                        ctx.beginPath();
                        ctx.moveTo(layerX[l], y1);
                        ctx.lineTo(layerX[l + 1], y2);
                        ctx.stroke();
                    }
                }
            }

            // Draw neurons
            for (let l = 0; l < layers.length; l++) {
                for (let i = 0; i < layers[l]; i++) {
                    const y = (h / 2) - ((layers[l] - 1) * neuronRadius * 2.5) / 2 + i * neuronRadius * 2.5;

                    const activation = playgroundState.activations[l] ? playgroundState.activations[l][i] : 0;

                    // Color based on activation
                    const normalized = Math.max(-1, Math.min(1, activation));
                    if (normalized > 0) {
                        const intensity = Math.floor(normalized * 255);
                        ctx.fillStyle = `rgb(${255 - intensity}, 255, ${255 - intensity})`;
                    } else {
                        const intensity = Math.floor(-normalized * 255);
                        ctx.fillStyle = `rgb(255, ${255 - intensity}, ${255 - intensity})`;
                    }

                    ctx.beginPath();
                    ctx.arc(layerX[l], y, neuronRadius, 0, 2 * Math.PI);
                    ctx.fill();
                    ctx.strokeStyle = '#1f2937';
                    ctx.lineWidth = 2;
                    ctx.stroke();

                    // Draw activation value
                    ctx.fillStyle = '#1f2937';
                    ctx.font = `bold ${neuronRadius * 0.7}px Inter`;
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(activation.toFixed(2), layerX[l], y);
                }
            }

            // Draw layer labels
            const labels = ['Input', ...Array(playgroundState.architecture.hidden.length).fill(0).map((_, i) => `Hidden ${i + 1}`), 'Output'];
            ctx.fillStyle = '#1f2937';
            ctx.font = 'bold 14px Inter';
            ctx.textAlign = 'center';
            for (let l = 0; l < layers.length; l++) {
                ctx.fillText(labels[l], layerX[l], h - 30);
            }

            updatePlaygroundMetrics();
            updatePlaygroundParametersTable();
        }

        function playgroundForwardPass() {
            playgroundState.activations = [playgroundState.inputs.slice()];

            for (let l = 0; l < playgroundState.weights.length; l++) {
                const prevActivations = playgroundState.activations[l];
                const nextActivations = [];

                for (let j = 0; j < playgroundState.weights[l][0].length; j++) {
                    let sum = playgroundState.biases[l][j];
                    for (let i = 0; i < prevActivations.length; i++) {
                        sum += prevActivations[i] * playgroundState.weights[l][i][j];
                    }
                    nextActivations.push(playgroundActivationFunc(sum, playgroundState.activation));
                }

                playgroundState.activations.push(nextActivations);
            }

            // Calculate loss (MSE)
            const output = playgroundState.activations[playgroundState.activations.length - 1];
            let loss = 0;
            for (let i = 0; i < output.length; i++) {
                loss += Math.pow(output[i] - playgroundState.target[i], 2);
            }
            playgroundState.currentLoss = loss / output.length;
        }

        function updatePlaygroundMetrics() {
            document.getElementById('pgSteps').textContent = playgroundState.steps;
            document.getElementById('pgLoss').textContent = playgroundState.currentLoss.toFixed(4);

            // Calculate average weight
            let sumWeights = 0;
            let countWeights = 0;
            for (const w of playgroundState.weights) {
                for (const row of w) {
                    for (const val of row) {
                        sumWeights += val;
                        countWeights++;
                    }
                }
            }
            document.getElementById('pgAvgWeight').textContent = (sumWeights / countWeights).toFixed(3);

            // Max gradient (if available)
            let maxGrad = 0;
            for (const g of playgroundState.gradients) {
                for (const row of g) {
                    for (const val of row) {
                        maxGrad = Math.max(maxGrad, Math.abs(val));
                    }
                }
            }
            document.getElementById('pgMaxGrad').textContent = maxGrad.toFixed(4);
        }

        function updatePlaygroundParametersTable() {
            const container = document.getElementById('pgParametersTable');
            let html = '<table style="width: 100%; border-collapse: collapse; color: var(--text-primary);">';
            html += '<thead><tr style="background: var(--bg-primary);"><th style="padding: 0.5rem; border: 1px solid var(--border-color); text-align: left;">Layer</th><th style="padding: 0.5rem; border: 1px solid var(--border-color); text-align: left;">Parameter</th><th style="padding: 0.5rem; border: 1px solid var(--border-color); text-align: left;">Shape</th><th style="padding: 0.5rem; border: 1px solid var(--border-color); text-align: left;">Sample Values</th></tr></thead>';
            html += '<tbody>';

            for (let l = 0; l < playgroundState.weights.length; l++) {
                const w = playgroundState.weights[l];
                const b = playgroundState.biases[l];

                // Weights
                html += `<tr style="background: ${l % 2 === 0 ? 'var(--bg-secondary)' : 'var(--bg-primary)'};">`;
                html += `<td style="padding: 0.5rem; border: 1px solid var(--border-color);">Layer ${l} → ${l + 1}</td>`;
                html += `<td style="padding: 0.5rem; border: 1px solid var(--border-color);">Weights (W)</td>`;
                html += `<td style="padding: 0.5rem; border: 1px solid var(--border-color);">${w.length} × ${w[0].length}</td>`;
                html += `<td style="padding: 0.5rem; border: 1px solid var(--border-color);">${w.slice(0, 2).map(row => '[' + row.slice(0, 3).map(v => v.toFixed(2)).join(', ') + (row.length > 3 ? ', ...' : '') + ']').join(', ')}${w.length > 2 ? ', ...' : ''}</td>`;
                html += '</tr>';

                // Biases
                html += `<tr style="background: ${l % 2 === 0 ? 'var(--bg-secondary)' : 'var(--bg-primary)'};">`;
                html += `<td style="padding: 0.5rem; border: 1px solid var(--border-color);">Layer ${l} → ${l + 1}</td>`;
                html += `<td style="padding: 0.5rem; border: 1px solid var(--border-color);">Biases (b)</td>`;
                html += `<td style="padding: 0.5rem; border: 1px solid var(--border-color);">${b.length}</td>`;
                html += `<td style="padding: 0.5rem; border: 1px solid var(--border-color);">[${b.slice(0, 5).map(v => v.toFixed(2)).join(', ')}${b.length > 5 ? ', ...' : ''}]</td>`;
                html += '</tr>';
            }

            html += '</tbody></table>';
            container.innerHTML = html;
        }

        function playgroundStepForward() {
            playgroundForwardPass();
            drawPlayground();
        }

        function playgroundStepBackward() {
            // Implement backpropagation
            playgroundBackpropagation();
            drawPlayground();
        }

        function playgroundBackpropagation() {
            // Compute gradients
            playgroundState.gradients = [];

            const output = playgroundState.activations[playgroundState.activations.length - 1];
            let delta = [];
            for (let i = 0; i < output.length; i++) {
                delta.push(2 * (output[i] - playgroundState.target[i]));
            }

            for (let l = playgroundState.weights.length - 1; l >= 0; l--) {
                const grads = [];
                for (let i = 0; i < playgroundState.weights[l].length; i++) {
                    const row = [];
                    for (let j = 0; j < playgroundState.weights[l][i].length; j++) {
                        row.push(playgroundState.activations[l][i] * delta[j]);
                    }
                    grads.push(row);
                }
                playgroundState.gradients.unshift(grads);

                // Propagate delta backwards
                const newDelta = [];
                for (let i = 0; i < playgroundState.weights[l].length; i++) {
                    let sum = 0;
                    for (let j = 0; j < playgroundState.weights[l][i].length; j++) {
                        sum += playgroundState.weights[l][i][j] * delta[j];
                    }
                    newDelta.push(sum);
                }
                delta = newDelta;
            }
        }

        function playgroundTrainStep() {
            playgroundForwardPass();
            playgroundBackpropagation();

            // Update weights
            for (let l = 0; l < playgroundState.weights.length; l++) {
                for (let i = 0; i < playgroundState.weights[l].length; i++) {
                    for (let j = 0; j < playgroundState.weights[l][i].length; j++) {
                        playgroundState.weights[l][i][j] -= playgroundState.learningRate * playgroundState.gradients[l][i][j];
                    }
                }
            }

            playgroundState.steps++;
            drawPlayground();
        }

        function playgroundTrain(steps) {
            for (let i = 0; i < steps; i++) {
                playgroundTrainStep();
            }
        }

'''

        content = content[:insert_before] + playground_js + content[insert_before:]

        # Add initialization in window.onload
        onload_end = content.find('};', match.end())
        if onload_end != -1:
            init_call = '''
            // Initialize playground
            if (document.getElementById('playgroundCanvas')) {
                initializePlaygroundWeights();
                updatePlaygroundInputControls();
                drawPlayground();
            }
'''
            content = content[:onload_end] + init_call + content[onload_end:]

        print("  [OK] Playground JavaScript added")
    else:
        print("  [WARNING] Could not find window.onload to add playground JS")

    return content

def main():
    filepath = r'C:\GitHub\me\nlp\kb\neural_networks_educational.html'

    print("="*60)
    print("Adding Playground and Display Elements")
    print("="*60)

    content = read_file(filepath)
    print(f"\nOriginal size: {len(content)} characters")

    content = add_display_elements(content)
    content = add_neural_playground(content)
    content = add_playground_javascript(content)

    write_file(filepath, content)
    print(f"New size: {len(content)} characters")

    print("\n" + "="*60)
    print("[SUCCESS] Playground and displays added!")
    print("="*60)

if __name__ == '__main__':
    main()
