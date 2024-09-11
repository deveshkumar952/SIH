// Function to handle file selection and display file info
document.addEventListener('DOMContentLoaded', function() {
    // Trigger the file input click when either browse-label or drag-here is clicked
    document.querySelector('.browse-label').addEventListener('click', function() {
        document.querySelector('#file').click();
    });

    document.querySelector('.drag-here').addEventListener('click', function() {
        document.querySelector('#file').click();
    });

    // Add an event listener to detect when a file is selected
    document.querySelector('#file').addEventListener('change', function() {
        // Get the selected file
        const fileInput = document.querySelector('#file');
        const fileInfo = document.querySelector('#file-info');
        
        // If a file is selected, display its name
        if (fileInput.files.length > 0) {
            const fileName = fileInput.files[0].name;
            fileInfo.textContent = `Selected file: ${fileName}`;
        } else {
            fileInfo.textContent = 'No file selected';
        }
    });
});
