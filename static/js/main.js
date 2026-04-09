document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-btn');
    const urlInput = document.getElementById('youtube-url');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const aiAnalysis = document.getElementById('ai-analysis');
    const transcriptText = document.getElementById('transcript-text');
    const statusMsg = document.getElementById('status-message');

    analyzeBtn.addEventListener('click', async () => {
        const url = urlInput.value.trim();
        if (!url) {
            showStatus("Please enter a valid YouTube URL.", "error");
            return;
        }

        // Reset UI
        showStatus("", "");
        results.classList.add('hidden');
        loading.classList.remove('hidden');
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "An error occurred while processing.");
            }

            // Update UI with results
            if (window.marked) {
                aiAnalysis.innerHTML = marked.parse(data.analysis_html);
            } else {
                aiAnalysis.textContent = data.analysis_html; 
            }
            transcriptText.textContent = data.transcript;

            // Render Metrics
            const qualityMetrics = document.getElementById('quality-metrics');
            if (data.metrics) {
                renderMetrics(data.metrics, qualityMetrics);
            } else {
                qualityMetrics.innerHTML = '<div class="metric-error">Evaluation failed or was skipped.</div>';
            }

            loading.classList.add('hidden');
            results.classList.remove('hidden');
            analyzeBtn.disabled = false;
            
        } catch (error) {
            showStatus(error.message, "error");
            loading.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    });

    function renderMetrics(metrics, container) {
        container.innerHTML = '';
        const metricKeys = Object.keys(metrics);
        
        metricKeys.forEach(key => {
            const m = metrics[key];
            const card = document.createElement('div');
            card.className = 'metric-card';
            
            const scoreClass = m.score >= 4 ? 'score-high' : (m.score >= 3 ? 'score-mid' : 'score-low');
            
            card.innerHTML = `
                <div class="metric-header">
                    <span class="metric-name">${key.charAt(0).toUpperCase() + key.slice(1)}</span>
                    <span class="metric-score ${scoreClass}">${m.score}/5</span>
                </div>
                <div class="metric-bar-bg">
                    <div class="metric-bar-fill ${scoreClass}" style="width: ${m.score * 20}%"></div>
                </div>
                <p class="metric-justification">${m.justification}</p>
            `;
            container.appendChild(card);
        });
    }

    function showStatus(text, type) {
        statusMsg.textContent = text;
        statusMsg.className = `status ${type}`;
    }
});

function showTab(tabId) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });

    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab and activate its button
    document.getElementById(tabId).classList.add('active');
    
    // Find button that calls this tabId
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => {
        if (btn.getAttribute('onclick').includes(tabId)) {
            btn.classList.add('active');
        }
    });
}
