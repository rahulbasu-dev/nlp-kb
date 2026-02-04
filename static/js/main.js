// ============================================================================
// NLP Classroom - Main JavaScript
// ============================================================================

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// ============================================================================
// Code Copying Functionality
// ============================================================================

function copyCode(button) {
    const codeBlock = button.closest('.code-container').querySelector('code');
    const text = codeBlock.textContent;
    
    navigator.clipboard.writeText(text).then(function() {
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> Copied!';
        button.classList.add('btn-success');
        
        setTimeout(function() {
            button.innerHTML = originalText;
            button.classList.remove('btn-success');
        }, 2000);
    });
}

// ============================================================================
// Interactive Demo - TF-IDF
// ============================================================================

function runTFIDFDemo() {
    const documents = [];
    const docInputs = document.querySelectorAll('.document-input');
    
    docInputs.forEach(input => {
        if (input.value.trim()) {
            documents.push(input.value.trim());
        }
    });
    
    if (documents.length < 2) {
        showAlert('Please enter at least 2 documents', 'warning');
        return;
    }
    
    showLoading('results-content');
    
    fetch('/demo/tfidf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ documents: documents })
    })
    .then(response => response.json())
    .then(data => {
        displayTFIDFResults(data);
    })
    .catch(error => {
        showError('results-content', error);
    });
}

function displayTFIDFResults(data) {
    const outputDiv = document.getElementById('results-content');
    const resultsSection = document.getElementById('results-section');
    const vizSection = document.getElementById('viz-section');
    
    if (data.status === 'error') {
        outputDiv.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
        resultsSection.style.display = 'block';
        vizSection.style.display = 'none';
        return;
    }
    
    let html = `
        <div class="row">
            <div class="col-lg-6">
                <h5 class="text-success mb-3"><i class="fas fa-list-ol"></i> Computation Steps</h5>
                <pre class="bg-light p-3 rounded" style="max-height: 500px; overflow-y: auto; font-size: 0.9em;"><code>${data.steps}</code></pre>
            </div>
            <div class="col-lg-6">
                <h5 class="text-success mb-3"><i class="fas fa-bar-chart"></i> Results</h5>
    `;
    
    data.results.forEach(result => {
        html += `
            <div class="mb-3">
                <h6 class="text-info">Document ${result.doc_id}</h6>
                <table class="table table-sm table-striped">
                    <thead>
                        <tr>
                            <th>Word</th>
                            <th>TF-IDF Score</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        result.top_words.forEach(item => {
            html += `
                <tr>
                    <td>${item.word}</td>
                    <td><span class="badge bg-success">${item.score}</span></td>
                </tr>
            `;
        });
        
        html += `
                    </tbody>
                </table>
            </div>
        `;
    });
    
    html += `
            </div>
        </div>
    `;
    
    outputDiv.innerHTML = html;
    resultsSection.style.display = 'block';
    
    // Display visualization if available
    if (data.visualization) {
        vizSection.style.display = 'block';
        Plotly.newPlot('tfidf-visualization', data.visualization.data, data.visualization.layout, {responsive: true});
        
        const vizInfo = document.getElementById('viz-info');
        const meta = data.viz_metadata || {};
        vizInfo.innerHTML = `
            <div class="row">
                <div class="col-md-4">
                    <p><strong>Documents:</strong> ${meta.num_documents}</p>
                </div>
                <div class="col-md-4">
                    <p><strong>Unique Words:</strong> ${meta.vocab_size}</p>
                </div>
                <div class="col-md-4">
                    <p><strong>Reduction Method:</strong> ${meta.method ? meta.method.toUpperCase() : 'PCA'}</p>
                </div>
            </div>
        `;
    } else {
        vizSection.style.display = 'none';
    }
}

// ============================================================================
// Interactive Demo - SGNS
// ============================================================================

function runSGNSDemo() {
    const corpus = [];
    const corpusInputs = document.querySelectorAll('.sentence-input');
    
    console.log('SGNS Demo: Found', corpusInputs.length, 'inputs');
    
    corpusInputs.forEach(input => {
        if (input.value.trim()) {
            corpus.push(input.value.trim());
        }
    });
    
    console.log('SGNS Demo: Corpus has', corpus.length, 'sentences');
    
    if (corpus.length < 2) {
        showAlert('Please enter at least 2 sentences', 'warning');
        return;
    }
    
    const params = {
        embedding_dim: parseInt(document.getElementById('embedding-dim')?.value || 50),
        window_size: parseInt(document.getElementById('window-size')?.value || 2),
        negative_samples: parseInt(document.getElementById('negative-samples')?.value || 5),
        epochs: parseInt(document.getElementById('epochs')?.value || 10)
    };
    
    console.log('SGNS Demo: Parameters', params);
    console.log('SGNS Demo: Sending request...');
    
    showLoading('sgns-results-content');
    
    fetch('/demo/sgns', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ corpus: corpus, params: params })
    })
    .then(response => {
        console.log('SGNS Demo: Response status', response.status);
        return response.json();
    })
    .then(data => {
        console.log('SGNS Demo: Response data', data);
        displaySGNSResults(data);
    })
    .catch(error => {
        console.error('SGNS Demo: Error', error);
        showError('sgns-results-content', error);
    });
}

function displaySGNSResults(data) {
    const outputDiv = document.getElementById('sgns-results-content');
    const resultsSection = document.getElementById('sgns-results-section');
    const vizSection = document.getElementById('sgns-viz-section');
    
    if (data.status === 'error') {
        outputDiv.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
        resultsSection.style.display = 'block';
        vizSection.style.display = 'none';
        return;
    }
    
    let html = `
        <div class="row">
            <div class="col-lg-6">
                <h5 class="text-primary mb-3"><i class="fas fa-list-ol"></i> Training Steps</h5>
                <pre class="bg-light p-3 rounded" style="max-height: 500px; overflow-y: auto; font-size: 0.9em;"><code>${data.steps}</code></pre>
            </div>
            <div class="col-lg-6">
                <h5 class="text-primary mb-3"><i class="fas fa-network-wired"></i> Learned Similarities</h5>
                <div class="mb-3">
                    <p><strong>Vocabulary Size:</strong> <span class="badge bg-info">${data.vocab_size}</span></p>
                    <p><strong>Training Pairs:</strong> <span class="badge bg-warning">${data.training_pairs}</span></p>
                </div>
    `;
    
    for (const [word, similarities] of Object.entries(data.similarities)) {
        html += `
            <div class="mb-3">
                <strong class="text-info">"${word}" is similar to:</strong><br>
                ${similarities.map(item => `
                    <span class="badge bg-success ms-1 mb-1">${item.word} (${item.score})</span>
                `).join('')}
            </div>
        `;
    }
    
    html += `
            </div>
        </div>
    `;
    
    outputDiv.innerHTML = html;
    resultsSection.style.display = 'block';
    
    // Display visualization if available
    if (data.visualization && vizSection) {
        vizSection.style.display = 'block';
        Plotly.newPlot('sgns-visualization', data.visualization.data, data.visualization.layout, {responsive: true});
        
        const vizInfo = document.getElementById('sgns-viz-info');
        if (vizInfo) {
            const meta = data.viz_metadata || {};
            vizInfo.innerHTML = `
                <div class="row">
                    <div class="col-md-4">
                        <p><strong>Vocabulary:</strong> ${meta.vocab_size} words</p>
                    </div>
                    <div class="col-md-4">
                        <p><strong>Embedding Dim:</strong> ${meta.embedding_dim}D</p>
                    </div>
                    <div class="col-md-4">
                        <p><strong>Reduction Method:</strong> ${meta.method ? meta.method.toUpperCase() : 'PCA'}</p>
                    </div>
                </div>
            `;
        }
    } else if (vizSection) {
        vizSection.style.display = 'none';
    }
}

// ============================================================================
// Utility Functions
// ============================================================================

function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('main').insertAdjacentElement('afterbegin', alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function showLoading(elementId) {
    const element = document.getElementById(elementId);
    element.innerHTML = `
        <div class="text-center py-5">
            <div class="loading-spinner mx-auto mb-3"></div>
            <p class="text-muted">Processing...</p>
        </div>
    `;
}

function showError(elementId, error) {
    const element = document.getElementById(elementId);
    element.innerHTML = `
        <div class="alert alert-danger">
            <i class="fas fa-exclamation-triangle"></i>
            Error: ${error.message || error}
        </div>
    `;
}

// ============================================================================
// Classroom Mode Functions
// ============================================================================

let currentSlide = 0;
let slides = [];

function initClassroom(slideList) {
    slides = slideList;
    currentSlide = 0;
    showSlide(currentSlide);
}

function showSlide(index) {
    if (index < 0 || index >= slides.length) return;
    
    currentSlide = index;
    const slide = slides[currentSlide];
    
    // Update image
    const imgElement = document.getElementById('classroom-viz');
    if (imgElement) {
        imgElement.src = `/visualization/${slide.file}`;
        imgElement.alt = slide.title;
    }
    
    // Update title
    const titleElement = document.getElementById('slide-title');
    if (titleElement) {
        titleElement.textContent = slide.title;
    }
    
    // Update indicator
    updateIndicator();
    
    // Update button states
    updateNavigationButtons();
}

function nextSlide() {
    if (currentSlide < slides.length - 1) {
        showSlide(currentSlide + 1);
    }
}

function prevSlide() {
    if (currentSlide > 0) {
        showSlide(currentSlide - 1);
    }
}

function updateIndicator() {
    const indicator = document.getElementById('slide-indicator');
    if (indicator) {
        indicator.textContent = `${currentSlide + 1} / ${slides.length}`;
    }
}

function updateNavigationButtons() {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    
    if (prevBtn) {
        prevBtn.disabled = currentSlide === 0;
    }
    
    if (nextBtn) {
        nextBtn.disabled = currentSlide === slides.length - 1;
    }
}

function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        }
    }
}

// Keyboard shortcuts for classroom mode
document.addEventListener('keydown', function(event) {
    if (window.location.pathname.includes('/classroom')) {
        switch(event.key) {
            case 'ArrowRight':
            case ' ':
                event.preventDefault();
                nextSlide();
                break;
            case 'ArrowLeft':
                event.preventDefault();
                prevSlide();
                break;
            case 'f':
                event.preventDefault();
                toggleFullscreen();
                break;
            case 'Escape':
                if (document.fullscreenElement) {
                    document.exitFullscreen();
                }
                break;
        }
    }
});

// ============================================================================
// Visualization Modal
// ============================================================================

function showVisualizationModal(filename, title) {
    const modal = document.getElementById('viz-modal');
    const img = document.getElementById('modal-viz-img');
    const titleEl = document.getElementById('modal-viz-title');
    
    if (img) img.src = `/visualization/${filename}`;
    if (titleEl) titleEl.textContent = title;
    
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
}

// ============================================================================
// Add Document Input Fields
// ============================================================================

function addDocumentInput(containerId = 'documents-container') {
    const container = document.getElementById(containerId);
    const count = container.querySelectorAll('textarea').length + 1;
    
    const div = document.createElement('div');
    div.className = 'mb-3';
    div.innerHTML = `
        <label class="form-label fw-bold">Document ${count}</label>
        <textarea class="form-control document-input" rows="3" 
                  placeholder="Enter document text..."></textarea>
    `;
    
    container.appendChild(div);
}

function addSentenceInput(containerId = 'corpus-container') {
    const container = document.getElementById(containerId);
    const count = container.querySelectorAll('input').length + 1;
    
    const div = document.createElement('div');
    div.className = 'mb-3';
    div.innerHTML = `
        <label class="form-label fw-bold">Sentence ${count}</label>
        <input type="text" class="form-control sentence-input" 
               placeholder="Enter sentence...">
    `;
    
    container.appendChild(div);
}

// ============================================================================
// Export Functions for Global Use
// ============================================================================

window.copyCode = copyCode;
window.runTFIDFDemo = runTFIDFDemo;
window.runSGNSDemo = runSGNSDemo;
window.initClassroom = initClassroom;
window.nextSlide = nextSlide;
window.prevSlide = prevSlide;
window.toggleFullscreen = toggleFullscreen;
window.showVisualizationModal = showVisualizationModal;
window.addDocumentInput = addDocumentInput;
window.addSentenceInput = addSentenceInput;
