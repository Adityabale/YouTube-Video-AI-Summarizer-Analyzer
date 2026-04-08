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

            loading.classList.add('hidden');
            results.classList.remove('hidden');
            analyzeBtn.disabled = false;
            
            // Re-render any markdown-like content if necessary, 
            // but the backend is already sending HTML.
            
        } catch (error) {
            showStatus(error.message, "error");
            loading.classList.add('hidden');
            analyzeBtn.disabled = false;
        }
    });

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
