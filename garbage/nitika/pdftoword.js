document.getElementById('pdf-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Simulate file conversion by using a timeout
    const resultContainer = document.getElementById('result-container');
    const downloadLink = document.getElementById('download-link');

    // Show a loading message (optional)
    downloadLink.textContent = 'Converting...';

    setTimeout(() => {
        // Simulate the conversion process
        const pdfInput = document.getElementById('pdf-input').files[0];
        
        if (pdfInput) {
            // Display the download link
            resultContainer.querySelector('h3').style.display = 'block';
            downloadLink.textContent = 'Download Word Document';
            downloadLink.href = '#'; // Set your download link here
            downloadLink.style.display = 'inline'; // Show the link
        } else {
            alert('Please upload a PDF file.');
        }
    }, 2000); // Simulate a 2-second conversion process
});
