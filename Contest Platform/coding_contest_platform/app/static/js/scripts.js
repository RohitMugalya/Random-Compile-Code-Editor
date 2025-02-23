// Function to shuffle an array (used for shuffling line numbers)
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

// Initialize the code editor with shuffled line numbers
function initializeCodeEditor() {
    const codeEditor = document.getElementById('code-editor');
    if (codeEditor) {
        const lineNumbers = Array.from({ length: 60 }, (_, i) => i + 1);
        const shuffledLines = shuffleArray(lineNumbers);

        // Clear existing content
        codeEditor.innerHTML = '';

        // Create text areas for each line
        shuffledLines.forEach((lineNumber, index) => {
            const lineDiv = document.createElement('div');
            lineDiv.className = 'd-flex';

            const lineNumberSpan = document.createElement('span');
            lineNumberSpan.className = 'text-muted me-2';
            lineNumberSpan.style.width = '30px';
            lineNumberSpan.textContent = lineNumber;

            const textArea = document.createElement('textarea');
            textArea.name = `code_line_${index + 1}`;
            textArea.className = 'form-control mb-1';
            textArea.rows = 1;

            lineDiv.appendChild(lineNumberSpan);
            lineDiv.appendChild(textArea);
            codeEditor.appendChild(lineDiv);
        });
    }
}

// Handle form submission for code submission
function handleCodeSubmission(event) {
    const form = event.target;
    const codeLines = Array.from(form.querySelectorAll('textarea'))
        .map(textarea => textarea.value)
        .join('\n');
    const codeInput = document.createElement('input');
    codeInput.type = 'hidden';
    codeInput.name = 'code';
    codeInput.value = codeLines;
    form.appendChild(codeInput);
}

// Add event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize the code editor
    initializeCodeEditor();

    // Handle code submission form
    const codeForm = document.querySelector('form[action*="submit_code"]');
    if (codeForm) {
        codeForm.addEventListener('submit', handleCodeSubmission);
    }
});