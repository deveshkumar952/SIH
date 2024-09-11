document.getElementById('speak-btn').addEventListener('click', function() {
    const text = document.getElementById('text-input').value;

    if (text.trim() !== '') {
        const speech = new SpeechSynthesisUtterance(text);
        speechSynthesis.speak(speech);
    } else {
        alert('Please enter some text.');
    }
});
