let editor;

function initializeEditor() {
    require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.43.0/min/vs' }});
    require(["vs/editor/editor.main"], function () {
        editor = monaco.editor.create(document.getElementById("editor"), {
            value: "def hello():\n    print('Hello, world!')",
            language: "python",
            theme: "vs-dark",
            lineNumbers: (lineNumber) => shuffledNumbers[lineNumber - 1] || lineNumber,
            automaticLayout: true
        });
    });
}

function submitCode() {
    const code = editor.getValue();

    fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, mapping: originalMapping })
    })
    .then(response => response.json())
    .then(data => {
        alert("Ordered Code:\n" + data.ordered_code);
    });
}

window.onload = initializeEditor;
