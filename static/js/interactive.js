// Interactive Documentation Functions
function switchTab(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
    });
    
    // Show selected tab
    document.getElementById(tabName).style.display = 'block';
    
    // Update active button
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[onclick="switchTab('${tabName}')"]`).classList.add('active');
}

// Live Preview for HTML Editor
const htmlEditor = document.getElementById('htmlEditor');
const previewResult = document.getElementById('previewResult');

htmlEditor.addEventListener('input', () => {
    try {
        previewResult.innerHTML = htmlEditor.value;
        // Clear any error indicators
        htmlEditor.classList.remove('error');
    } catch (e) {
        // Add error indication
        htmlEditor.classList.add('error');
    }
});

// Challenge Verification with improved feedback
function checkChallenge() {
    const solution = htmlEditor.value.toLowerCase();
    const required = ['<h1', '<img', '<p', '<ul>'];
    
    // Create feedback array to track missing elements
    const missing = required.filter(element => !solution.includes(element));
    
    if (missing.length === 0) {
        showFeedback('success', "Great job! You've completed the challenge!", 'All required elements are present.');
    } else {
        showFeedback('error', 'Keep trying!', `Missing elements: ${missing.join(', ')}`);
    }
}

// Feedback display function
function showFeedback(type, title, message) {
    const feedbackDiv = document.createElement('div');
    feedbackDiv.className = `feedback-modal ${type}`;
    
    feedbackDiv.innerHTML = `
        <div class="feedback-content">
            <div class="feedback-header">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
                <h3>${title}</h3>
            </div>
            <p>${message}</p>
            <button onclick="this.parentElement.parentElement.remove()" class="feedback-btn">
                ${type === 'success' ? 'Continue' : 'Try Again'}
            </button>
        </div>
    `;
    
    document.body.appendChild(feedbackDiv);
    
    // Auto-remove feedback after 5 seconds
    setTimeout(() => {
        if (feedbackDiv.parentElement) {
            feedbackDiv.remove();
        }
    }, 5000);
} 