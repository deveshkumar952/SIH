document.getElementById('repair-btn').addEventListener('click', function() {
    const fileInput = document.getElementById('file-input');
    const outputContainer = document.getElementById('output-container');
    const outputText = document.getElementById('output-text');

    if (fileInput.files.length === 0) {
        alert('Please select a document to repair.');
        return;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = function(event) {
        let text = event.target.result;

        // Basic "repair" operations
        text = text.replace(/\r\n|\r/g, "\n"); // Normalize line endings
        text = text.replace(/\uFFFD/g, ""); // Remove replacement characters
        text = text.replace(/\s{2,}/g, ' '); // Replace multiple spaces with a single space

        outputText.value = text;
        outputContainer.style.display = 'block';
    };

    if (file.name.endsWith('.txt')) {
        reader.readAsText(file);
    } else if (file.name.endsWith('.docx')) {
        alert('Basic DOCX repair is not implemented in this example. Please upload a TXT file.');
        outputContainer.style.display = 'none';
    } else {
        alert('Unsupported file type. Please upload a TXT or DOCX file.');
        outputContainer.style.display = 'none';
    }
});
